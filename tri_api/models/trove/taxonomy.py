from beanie import Document
from typing import List, Optional
from pydantic import Field, BaseModel


class CWE(Document):
    id: str
    data: Optional[dict] = Field(default_factory=dict)
    child: Optional[dict] = Field(default_factory=dict)
    relation: Optional[dict] = Field(default_factory=dict)


class ListCWE:
    total_count: int = Field(default=0)
    cwe: List[CWE] = Field(default=[])
    has_next: bool = Field(default=False)


class CAPEC(Document):
    id: str
    data: Optional[dict] = Field(default_factory=dict)
    child: Optional[dict] = Field(default_factory=dict)
    relation: Optional[dict] = Field(default_factory=dict)


class ListCAPEC:
    total_count: int = Field(default=0)
    cwe: List[CAPEC] = Field(default=[])
    has_next: bool = Field(default=False)
