# Axionorm

**Agent policy as code**. A YAML-first initiative for describing agent authority and governance independently of any one agent product.

## Status

Early-stage specification and planning. No stable schema, evaluator, or OPA/Rego integration is released yet.

## Scope

- Explicit agent authority, allowed capabilities, and target scope.
- Approval requirements and policy decision records.
- Portable policy documents with validation and versioning.
- A planned optional OPA/Rego evaluation backend.

## Initial roadmap

1. Review the existing policy prototype in [Lophiarch](https://github.com/amiencoy/lophiarch), formerly Reconnator: `src/config/agent-policy.yaml`.
2. Separate product-specific configuration from a reusable policy specification.
3. Draft a schema and examples, including invalid and denied cases.
4. Define an evaluator contract and explore an optional OPA/Rego backend.
5. Integrate with consumers after the specification and compatibility requirements are reviewed.

The existing Lophiarch policy has not been migrated by creating this repository.

## Boundaries

Axionorm defines policy. Agent runtimes enforce policy decisions. [Parabiont Protocol](https://github.com/amiencoy/parabiont-protocol) addresses governed attachment; Lophiarch remains a reconnaissance product.

## Contributing

Open issues for use cases, policy semantics, and schema proposals. Mark draft requirements explicitly and include expected allow/deny outcomes in examples.

## Licensing

Licensing for the specification and future implementations remains to be selected.
