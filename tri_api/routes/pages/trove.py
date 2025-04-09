from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from tri_api.support.enums import TemplatePath, TroveRouteEnum


router = APIRouter(
    tags=["trove"],
)


templates = Jinja2Templates(
    directory=TemplatePath.template_dir.value,
)


@router.get(TroveRouteEnum.trove.value)
def serve_home(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name=TemplatePath.trove.value,
    )
