from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class ContextPolicy(Strict):
    topics: list[str] = Field(min_length=1, max_length=30)
    kinds: list[Literal["fact", "decision", "task", "constraint"]]
    denied_labels: list[str] = Field(min_length=1)
    max_items: int = Field(default=100, ge=1, le=500)
    max_item_chars: int = Field(default=2000, ge=1, le=10000)


class ToolRule(Strict):
    name: Literal["workspace_list", "workspace_read", "workspace_write", "context_read"]
    allow: bool = False
    extensions: list[str] = Field(default_factory=list)
    max_bytes: int = Field(default=32768, ge=1, le=1048576)


class Policy(Strict):
    version: Literal["axionorm/v0.1"]
    policy_id: str = Field(pattern=r"^[a-z0-9-]{1,64}$")
    audience: str = Field(pattern=r"^[a-z0-9-]{1,64}$")
    purpose: str = Field(pattern=r"^[a-z0-9-]{1,64}$")
    lease_seconds: int = Field(default=600, ge=30, le=3600)
    context: ContextPolicy
    tools: list[ToolRule]


class Item(Strict):
    id: str = Field(pattern=r"^[a-zA-Z0-9-]{1,64}$")
    kind: Literal["fact", "decision", "task", "constraint"]
    topic: str = Field(pattern=r"^[a-z0-9-]{1,64}$")
    labels: list[str] = Field(min_length=1, max_length=20)
    text: str = Field(min_length=1, max_length=10000)


class Candidate(Strict):
    version: Literal["parabiont-candidate/v0.1"]
    items: list[Item] = Field(min_length=1, max_length=500)
