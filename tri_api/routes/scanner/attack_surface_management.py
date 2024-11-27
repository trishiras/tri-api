from typing import List
from tri_api.models.tenant.user import User
from tri_api.support.current_user import current_user
from fastapi import (
    Query,
    Depends,
    Response,
    APIRouter,
    HTTPException,
)
from tri_api.models.scanner.task import (
    ScannerTask,
    ScannerTaskArguments,
    PaginatedScannerTaskResponse,
)
from tri_api.support.enums import (
    TargetType,
    RouteEnum,
    ScannerType,
    ResponseCode,
    ScannerStatus,
    ScannerRouteEnum,
    ScannerExceptionMessage,
)


router = APIRouter(
    prefix=RouteEnum.api.value + ScannerRouteEnum.scanner.value,
    tags=["scanner"],
)


@router.post(
    ScannerRouteEnum.attack_surface_management.value,
)
async def create_attack_surface_management_task(
    arguments: ScannerTaskArguments,
    user: User = Depends(current_user),
):
    if arguments.target_type not in [
        TargetType.domain.value,
        TargetType.url.value,
        TargetType.ip.value,
        TargetType.cidr.value,
    ]:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ScannerExceptionMessage.incorrect_input.value,
        )

    scanner_task = ScannerTask(
        user=user.id,
        target=arguments.target,
        target_type=arguments.target_type,
        scanner_data=arguments.scanner_data,
        status=ScannerStatus.scheduled.value,
        scanner=ScannerType.attack_surface_management.value,
    )
    await scanner_task.create()

    return Response(status_code=ResponseCode.success.value)


@router.get(
    ScannerRouteEnum.attack_surface_management.value,
    response_model=PaginatedScannerTaskResponse,
    response_model_exclude_unset=True,
)
async def get_attack_surface_management_tasks(
    user: User = Depends(current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(3, ge=1, le=10),
) -> List[ScannerTask]:

    skip = (page - 1) * page_size

    total_tasks = await ScannerTask.find(
        ScannerTask.user == user.id,
        ScannerTask.scanner == ScannerType.attack_surface_management.value,
    ).count()

    tasks = (
        await ScannerTask.find(
            ScannerTask.user == user.id,
            ScannerTask.scanner == ScannerType.attack_surface_management.value,
        )
        .skip(skip)
        .limit(page_size)
        .to_list()
    )

    return {
        "total": total_tasks,
        "page_number": page,
        "data": tasks,
    }
