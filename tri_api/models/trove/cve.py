from beanie import Document
from typing import List, Optional, Dict
from pydantic import (
    Field,
    BaseModel,
    RootModel,
)


class CPE(BaseModel):
    cpe_string: str
    part: Optional[str] = Field(default_factory=str)
    vendor: Optional[str] = Field(default_factory=str)
    product: Optional[str] = Field(default_factory=str)
    version: Optional[str] = Field(default_factory=str)


class Reference(BaseModel):
    source: Optional[str] = Field(default_factory=str)
    type: str = Field(default_factory=str)
    url: str


class Remediation(BaseModel):
    source: str
    description: str
    references: List[Reference] = Field(default_factory=list)


class Exploits(BaseModel):
    exploit_available: bool = Field(default=False)
    references: List[Reference] = Field(default_factory=list)


class Zeroday(BaseModel):
    is_zeroday: bool = Field(default=False)
    references: List[Reference] = Field(default_factory=list)


class OWASP(BaseModel):
    owasp_id: Optional[str] = Field(default_factory=str)
    name: Optional[str] = Field(default_factory=str)
    description: Optional[str] = Field(default_factory=str)


class WASC(BaseModel):
    wasc_id: str
    name: Optional[str] = Field(default_factory=str)
    description: Optional[str] = Field(default_factory=str)


class WASCData(RootModel):
    root: Dict[str, WASC] = Field(default_factory=dict)


class CAPEC(BaseModel):
    capec_id: str
    name: Optional[str] = Field(default_factory=str)
    description: Optional[str] = Field(default_factory=str)
    domains_of_attack: List[str] = Field(default_factory=list)
    mechanisms_of_attack: List[str] = Field(default_factory=list)


class CAPECData(RootModel):
    root: Dict[str, CAPEC] = Field(default_factory=dict)


class CWE(BaseModel):
    cwe_id: str
    name: Optional[str] = Field(default_factory=str)
    description: Optional[str] = Field(default_factory=str)


class CWEData(RootModel):
    root: Dict[str, CWE] = Field(default_factory=dict)


class CVSS(BaseModel):
    version: str
    severity: Optional[int] = Field(default_factory=int)
    score: Optional[float] = Field(default_factory=float)
    vector: Optional[str] = Field(default_factory=str)


class CVSSData(RootModel):
    root: Dict[str, CVSS] = Field(default_factory=dict)


class Taxonomy(BaseModel):
    cvss: Optional[CVSSData] = Field(default_factory=CVSSData)
    cwe: Optional[CWEData] = Field(default_factory=CWEData)
    cpes: List[CPE] = Field(default_factory=list)
    wasc: Optional[WASCData] = Field(default_factory=WASCData)
    capec: Optional[CAPECData] = Field(default_factory=CAPECData)
    owasp: List[OWASP] = Field(default_factory=list)


class CVE(Document):
    id: str
    title: Optional[str] = Field(default_factory=str)
    description: Optional[str] = Field(default_factory=str)
    exploits: Optional[Exploits] = Field(default_factory=Exploits)
    zeroday: Optional[Zeroday] = Field(default_factory=Zeroday)
    seen_wild: bool = Field(default=False)
    priority_score: Optional[float] = Field(default=None)
    epss_score: Optional[float] = Field(default=None)
    taxonomy: Optional[Taxonomy] = Field(default_factory=Taxonomy)
    remediations: List[Remediation] = Field(default_factory=list)


class ListCVE:
    total_count: int = Field(default=0)
    cwe: List[CVE] = Field(default=[])
    has_next: bool = Field(default=False)
