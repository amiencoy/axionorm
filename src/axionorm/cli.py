import argparse
import json
from pathlib import Path
from .engine import Engine, digest
from .models import Candidate, Policy
from .install import install


def main():
    parser = argparse.ArgumentParser(description="Axionorm policy enforcement")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("install-opa")
    p.add_argument("--directory", default=".runtime/opa")
    p = sub.add_parser("review", help="After reviewing candidate text, approve selected item IDs")
    p.add_argument("candidate")
    p.add_argument("--approve", nargs="+", required=True)
    p.add_argument("--out", required=True)
    p = sub.add_parser("filter")
    p.add_argument("candidate")
    p.add_argument("--review", required=True)
    p.add_argument("--policy", required=True)
    p.add_argument("--opa", required=True)
    p = sub.add_parser("schema")
    p.add_argument("kind", choices=["policy", "candidate"])
    args = parser.parse_args()
    if args.command == "install-opa":
        print(install(args.directory))
    elif args.command == "schema":
        print(json.dumps((Policy if args.kind == "policy" else Candidate).model_json_schema(), indent=2))
    elif args.command == "review":
        candidate = Candidate.model_validate_json(Path(args.candidate).read_text()).model_dump()
        ids = set(args.approve)
        if not ids <= {i["id"] for i in candidate["items"]}:
            parser.error("Unknown item ID")
        review = {"version": "axionorm-review/v0.1", "approved": {
            i["id"]: digest(i) for i in candidate["items"] if i["id"] in ids}}
        with open(args.out, "x", encoding="utf-8") as stream:
            json.dump(review, stream, indent=2)
    else:
        engine = Engine(args.policy, args.opa)
        context, audit = engine.filter_context(json.loads(Path(args.candidate).read_text()),
                                               json.loads(Path(args.review).read_text()))
        print(json.dumps({"context": context, "audit": audit}, indent=2))
