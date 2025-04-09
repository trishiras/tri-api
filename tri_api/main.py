## Tri api
from tri_api.app import app


## Page Routers
from tri_api.routes.pages.home import router as HomePageRouter
from tri_api.routes.pages.trove import router as TrovePageRouter


## Super Routers
from tri_api.routes.super.tasks import router as TaskRouter
from tri_api.routes.super.user import router as SuperUserRouter


## Tenant Routers
from tri_api.routes.tenant.user import router as UserRouter
from tri_api.routes.tenant.mail import router as MailRouter
from tri_api.routes.tenant.register import router as RegisterRouter
from tri_api.routes.tenant.authorization import router as AuthRouter


## Trove Routers
from tri_api.routes.trove.intel import router as TroveIntelRouter


## Scanner Routers
from tri_api.routes.scanner.attack_surface_analysis import (
    router as AttackSurfaceAnalysisRouter,
)
from tri_api.routes.scanner.attack_surface_discovery import (
    router as AttackSurfaceDiscoveryRouter,
)
from tri_api.routes.scanner.attack_surface_management import (
    router as AttackSurfaceManagementRouter,
)
from tri_api.routes.scanner.cloud_security_posture_management import (
    router as CloudSecurityPostureManagementRouter,
)
from tri_api.routes.scanner.dynamic_application_security_testing import (
    router as DynamicApplicationSecurityTestingRouter,
)
from tri_api.routes.scanner.secret_exposure_analysis import (
    router as SecretExposureAnalysisRouter,
)
from tri_api.routes.scanner.software_bill_of_materials import (
    router as SoftwareBillOfMaterialsRouter,
)
from tri_api.routes.scanner.software_composition_analysis import (
    router as SoftwareCompositionAnalysisRouter,
)
from tri_api.routes.scanner.static_application_security_testing import (
    router as StaticApplicationSecurityTestingRouter,
)


## API Registered Routers


#
app.include_router(HomePageRouter)
app.include_router(TrovePageRouter)

#
app.include_router(TaskRouter)
app.include_router(SuperUserRouter)
#
app.include_router(AuthRouter)
app.include_router(MailRouter)
app.include_router(UserRouter)
app.include_router(RegisterRouter)
#
app.include_router(TroveIntelRouter)
#
app.include_router(AttackSurfaceAnalysisRouter)
app.include_router(AttackSurfaceDiscoveryRouter)
app.include_router(AttackSurfaceManagementRouter)
app.include_router(CloudSecurityPostureManagementRouter)
app.include_router(DynamicApplicationSecurityTestingRouter)
app.include_router(SecretExposureAnalysisRouter)
app.include_router(SoftwareBillOfMaterialsRouter)
app.include_router(SoftwareCompositionAnalysisRouter)
app.include_router(StaticApplicationSecurityTestingRouter)
