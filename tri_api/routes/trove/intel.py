from tri_api.models.trove.cve import CVE
from tri_api.models.tenant.user import User
from tri_api.models.trove.taxonomy import CWE, CAPEC
from tri_api.support.current_user import current_user
from fastapi import APIRouter, HTTPException, Depends
from tri_api.support.enums import (
    RouteEnum,
    ResponseCode,
    TroveRouteEnum,
    ExceptionMessage,
)


router = APIRouter(
    prefix=RouteEnum.api.value + TroveRouteEnum.trove.value,
    tags=["trove"],
)


@router.get(TroveRouteEnum.cwe.value, response_model=CWE)
async def get_cwe_by_id(
    cwe_id: str,
    user: User = Depends(current_user),
):

    cwe = await CWE.find_one(CWE.id == cwe_id)
    if cwe is None:
        raise HTTPException(
            status_code=ResponseCode.no_content.value,
            detail=ExceptionMessage.item_not_found.value,
        )

    return cwe


@router.get(TroveRouteEnum.capec.value, response_model=CAPEC)
async def get_capec_by_id(
    capec_id: str,
    user: User = Depends(current_user),
):

    capec = await CAPEC.find_one(CAPEC.id == capec_id)
    if capec is None:
        raise HTTPException(
            status_code=ResponseCode.no_content.value,
            detail=ExceptionMessage.item_not_found.value,
        )

    return capec


@router.get(TroveRouteEnum.cve.value, response_model=CVE)
async def get_cve_by_id(
    cve_id: str,
    user: User = Depends(current_user),
):

    if not user:
        return {}

    cve = await CVE.find_one(CVE.id == cve_id)
    if cve is None:
        raise HTTPException(
            status_code=ResponseCode.no_content.value,
            detail=ExceptionMessage.item_not_found.value,
        )

    return cve
