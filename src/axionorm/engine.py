import hashlib
import json
import re
import subprocess
from pathlib import Path
import yaml
from .models import Policy, Candidate


class PolicyDenied(RuntimeError):
    pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


# Defense in depth; not a semantic classifier. Explicit digest review remains mandatory.
SENSITIVE = re.compile(
    r"(?i)(-----BEGIN .{0,20}PRIVATE KEY|\b(?:password|api[_ -]?key|bearer|utang|hutang|pacar)\b"
    r"|[\w.+-]+@[\w.-]+\.[a-z]{2,}|\bsk-[A-Za-z0-9]{16,}"
    r"|ignore\s+(?:all|previous|the)\s+(?:instructions|policy|firewall)"
    r"|bypass\s+(?:the\s+)?(?:policy|firewall))"
)


class Engine:
    def __init__(self, policy_path, opa_path):
        raw = yaml.safe_load(Path(policy_path).read_text())
        self.policy = Policy.model_validate(raw).model_dump()
        names = [r["name"] for r in self.policy["tools"]]
        if len(names) != len(set(names)):
            raise PolicyDenied("Duplicate tool rules")
        self.opa = str(Path(opa_path).resolve(strict=True))
        self.policy_digest = digest(self.policy)

    def decide(self, request):
        payload = {**request, "policy": self.policy}
        try:
            result = subprocess.run(
                [self.opa, "eval", "--format=json", "--stdin-input", "--data",
                 str(Path(__file__).with_name("decision.rego")), "data.axionorm.allow"],
                input=canonical(payload), capture_output=True, timeout=5, check=True,
            )
            value = json.loads(result.stdout)["result"][0]["expressions"][0]["value"]
            return value is True
        except (OSError, subprocess.SubprocessError, ValueError, KeyError, IndexError):
            raise PolicyDenied("OPA unavailable or invalid decision; request denied") from None

    def filter_context(self, candidate, review):
        checked = Candidate.model_validate(candidate).model_dump()
        if len(checked["items"]) > self.policy["context"]["max_items"]:
            raise PolicyDenied("Context item limit exceeded")
        ids = [x["id"] for x in checked["items"]]
        if len(ids) != len(set(ids)):
            raise PolicyDenied("Duplicate context IDs")
        if set(review) != {"version", "approved"} or review["version"] != "axionorm-review/v0.1" or not isinstance(review["approved"], dict):
            raise PolicyDenied("Invalid review manifest")
        kept, audit = [], []
        for item in checked["items"]:
            allowed = self.decide({"action": "context", "item": item,
                                   "reviewed": review["approved"].get(item["id"]) == digest(item),
                                   "sensitive": self.sensitive(item["text"])})
            audit.append({"id": item["id"], "allowed": allowed})
            if allowed:
                kept.append({k: item[k] for k in ("id", "kind", "topic", "text")})
        if not kept:
            raise PolicyDenied("No approved relevant context")
        return kept, {"policy_digest": self.policy_digest, "decisions": audit}

    @staticmethod
    def sensitive(text):
        return bool(SENSITIVE.search(text))

    def authorize_tool(self, name, *, extension="", size=0, scope_valid=False):
        if type(size) is not int or size < 0 or not self.decide({"action": "tool", "tool": name,
            "extension": extension, "bytes": size, "scope_valid": scope_valid}):
            raise PolicyDenied("Tool or scope denied")
