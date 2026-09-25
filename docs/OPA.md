# Axionorm and OPA

Axionorm is the agent-specific policy authoring and enforcement layer. OPA is the general-purpose policy decision engine. They are complementary, not separate engines that compete over different policy domains.

| Concern | Axionorm | OPA |
| --- | --- | --- |
| Authoring | Validates YAML with a strict, versioned schema | Evaluates the packaged Rego rules against normalized JSON |
| Context | Checks reviewed content digests and sensitive patterns; constructs filtered output | Decides allow/deny per item using relevance, labels, review and limits |
| Tools | Validates paths and content; blocks execution at MCP boundary | Decides allow/deny for the operation, extension, size and scope |
| Lifecycle | Binds policy digest to a Parabiont lease and checks every tool call | Evaluates current rules without handling provider state |
| Failure | Blocks if OPA times out, fails, or returns an unexpected result | No permissive fallback |

The decision paths are `action=context` and `action=tool`. OPA does not infer private facts, understand natural-language relevance, remove text, install tools, or enforce anything in a provider account. Axionorm performs selection and enforcement. YAML describes authority, not an Ansible playbook that executes arbitrary installation commands.

`axionorm install-opa --directory .runtime/opa` installs OPA 1.19.1 locally, without sudo or global PATH changes. SHA-256 digests in `opa-lock.json` come from official release assets. Matching binaries are reused. The lock covers Linux AMD64/ARM64, macOS AMD64/ARM64 and Windows AMD64. The protected MCP filesystem gateway currently requires POSIX (Linux/macOS/WSL2).

OPA runs as a local subprocess per decision. There is no public OPA API. A future high-throughput deployment can use a localhost sidecar or embedded/Wasm evaluator with the same contract. No production latency or compliance certification is claimed.

Privacy uses reviewed content digests, explicit allowlists and conservative text checks. Pattern matching is not a complete semantic detector. A reviewer approving mislabeled sensitive prose can still authorize disclosure. Keep reviews and signing keys inaccessible to agents, inspect the outgoing packet, and never automatically approve a full chat export.

References: https://www.openpolicyagent.org/docs/deploy , https://www.openpolicyagent.org/docs/integration , https://www.openpolicyagent.org/docs/cli , https://github.com/open-policy-agent/opa/releases/tag/v1.19.1
