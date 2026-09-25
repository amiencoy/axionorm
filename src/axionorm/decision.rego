package axionorm
import rego.v1

default allow := false

allow if {
    input.action == "context"
    input.reviewed == true
    input.sensitive == false
    input.item.topic in input.policy.context.topics
    input.item.kind in input.policy.context.kinds
    "technical" in input.item.labels
    count(input.item.text) <= input.policy.context.max_item_chars
    not denied_label
}

denied_label if {
    some label in input.item.labels
    label in input.policy.context.denied_labels
}

allow if {
    input.action == "tool"
    input.scope_valid == true
    some rule in input.policy.tools
    rule.name == input.tool
    rule.allow == true
    input.bytes <= rule.max_bytes
    extension_ok(rule)
}

extension_ok(rule) if { input.tool in {"workspace_list", "context_read"} }
extension_ok(rule) if { input.extension in rule.extensions }
