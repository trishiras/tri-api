from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from tri_api.support.enums import RouteEnum, TemplatePath


router = APIRouter(
    tags=["home"],
)


templates = Jinja2Templates(
    directory=TemplatePath.template_dir.value,
)


@router.get(RouteEnum.home.value)
def serve_home(
    request: Request,
):
    return templates.TemplateResponse(
        request=request,
        name=TemplatePath.home.value,
    )
