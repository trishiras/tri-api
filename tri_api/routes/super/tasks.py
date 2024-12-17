import secrets
from tri_api.models.tenant.user import User
from fastapi import Query, APIRouter, Response, HTTPException
from tri_api.support.current_super_user import current_super_user
from tri_api.models.tenant.tenant import (
    InviteToken,
    ActiveTokenList,
)
from tri_api.celery.tasks import (
    populate_trove_intel_database,
)
from tri_api.models.scanner.task import (
    ScannerTask,
    ScannerTaskBase,
    ScannerTaskUpdate,
    PaginatedScannerTaskResponse,
)
from tri_api.support.enums import (
    RouteEnum,
    ResponseCode,
    ExceptionMessage,
    ScannerRouteEnum,
)
from tri_api.models.super.user import (
    SuperUserLogin,
    SuperUserMemberUpdate,
)


router = APIRouter(
    prefix=RouteEnum.api.value + RouteEnum.super_user.value + RouteEnum.tasks.value,
    tags=["Tasks"],
)


@router.get(RouteEnum.populate_database.value)
async def database_update(super_user_login: SuperUserLogin) -> Response:

    super_user = await current_super_user(
        super_user_login=super_user_login,
    )

    populate_trove_intel_database.apply_async(
        queue="tri",
        exchange="tri",
        routing_key="tri",
    )

    return Response(status_code=200)


@router.post(RouteEnum.token.value)
async def create_token(super_user_login: SuperUserLogin):

    super_user = await current_super_user(
        super_user_login=super_user_login,
    )

    existing_token = await InviteToken.find(
        InviteToken.status == True,
        InviteToken.user == None,
    ).to_list()

    number_of_tokens_to_create = 10 - len(existing_token)

    for _ in range(number_of_tokens_to_create):
        token = secrets.token_urlsafe(9)
        invite_token = InviteToken(token=token)
        await invite_token.create()

    return Response(status_code=200)


@router.get(RouteEnum.token.value, response_model=ActiveTokenList)
async def get_active_tokens(super_user_login: SuperUserLogin) -> ActiveTokenList:

    super_user = await current_super_user(
        super_user_login=super_user_login,
    )

    return await ActiveTokenList.get_token_list()


@router.get(RouteEnum.user.value, response_model=list[User])
async def get_users(super_user_login: SuperUserLogin) -> list[User]:

    super_user = await current_super_user(
        super_user_login=super_user_login,
    )

    return await User.get_all_users()


@router.post(RouteEnum.update_member.value, response_model=User)
async def update_member(
    super_user_member_update: SuperUserMemberUpdate,
):

    super_user_login = SuperUserLogin(
        id=super_user_member_update.id,
        password=super_user_member_update.password,
        login_key=super_user_member_update.login_key,
    )

    super_user = await current_super_user(
        super_user_login=super_user_login,
    )

    return await User.update_member(
        super_user_member_update.user_id,
        super_user_member_update.disable,
    )


@router.get(
    ScannerRouteEnum.scanner.value + RouteEnum.fetch_task.value,
    response_model=PaginatedScannerTaskResponse,
    response_model_exclude_unset=True,
)
async def get_tasks_list(
    super_user_login: SuperUserLogin,
    status: str = Query(None),
    synced: bool = Query(False),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=100),
) -> PaginatedScannerTaskResponse:

    super_user = await current_super_user(
        super_user_login=super_user_login,
    )

    skip = (page - 1) * page_size

    total_tasks = await ScannerTask.find(
        ScannerTask.status == status,
        ScannerTask.synced == synced,
    ).count()

    tasks = (
        await ScannerTask.find(
            ScannerTask.status == status,
            ScannerTask.synced == synced,
        )
        .skip(skip)
        .limit(page_size)
        .to_list()
    )

    return {
        "total": total_tasks,
        "page_number": page,
        "data": list(tasks),
    }


@router.post(
    ScannerRouteEnum.scanner.value + RouteEnum.update_task.value,
    response_model=ScannerTask,
)
async def update_task(
    scanner_task_update: ScannerTaskUpdate,
):

    super_user_login = SuperUserLogin(
        id=scanner_task_update.id,
        password=scanner_task_update.password,
        login_key=scanner_task_update.login_key,
    )
    task = ScannerTaskBase(
        task_id=scanner_task_update.task_id,
        status=scanner_task_update.status,
        result_url=scanner_task_update.result_url,
        status_message=scanner_task_update.status_message,
        synced=scanner_task_update.synced,
    )

    super_user = await current_super_user(
        super_user_login=super_user_login,
    )

    return await ScannerTask.update_task(task=task)
