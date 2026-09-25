# Axionorm

**Agent policy as code.** YAML-first authority and context policy with an installable Python reference implementation and OPA backend.

## Status

v0.1.0 is an experimental reference implementation: strict schemas, digest-bound context review, a real OPA/Rego evaluator, and enforcement integrated with Parabiont and PARALAX MCP. It is not a complete semantic DLP product or a production security certification.

## Install

Python 3.11+ and Git are required. Use a virtual environment.

```bash
git clone --branch v0.1.0 https://github.com/amiencoy/axionorm.git
cd axionorm
python3 -m venv .venv
. .venv/bin/activate
python -m pip install .
axionorm install-opa --directory .runtime/opa
axionorm schema policy
```

OPA installs locally with a pinned version and verified checksum. See [OPA mechanics](docs/OPA.md). YAML does not execute arbitrary installation stages.

## Review and filter

Read candidate JSON before approving selected IDs. Approval records content digests; subsequent edits invalidate approval.

```bash
axionorm review candidate.json --approve architecture continuity --out review.local.json
axionorm filter candidate.json --review review.local.json --policy examples/technical-review.yaml --opa .runtime/opa/opa
```

Eligible records are `fact`, `decision`, `task`, and `constraint` in approved topics. Personal labels, unreviewed items, unknown fields, suspicious text, missing OPA and invalid decisions fail closed. The sample policy disables writes; operators can enable bounded artifact creation before issuing a new capsule.

## Integration

- [Parabiont Protocol](https://github.com/amiencoy/parabiont-protocol): signed, leased context carrier over A2A.
- [PARALAX MCP](https://github.com/amiencoy/paralax-mcp): tool scope/output enforcement, combined installer and desktop setup.
- [Lophiarch](https://github.com/amiencoy/lophiarch): separate reconnaissance product. Its existing policy has not been migrated.

Install pytest, then run `python -m pytest tests -q` after installing OPA. `OPA_BINARY` overrides its location. Schemas are available in `schemas/` and through the CLI.

## Licensing

Licensing for the specification and implementations remains to be selected. Dependencies retain their upstream licenses.

---

<p align="center"><sub>Built with code, coffee, and a healthy dislike of repetitive work.</sub></p>
