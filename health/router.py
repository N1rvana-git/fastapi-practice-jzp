from fastapi import APIRouter, Depends
from . import dependencies
from . import schemas

router = APIRouter(
    tags=["health check"]
)

@router.get(
    "/health",
    response_model=schemas.HealthCheckResponse,
)

async def health_check(
        _ping :None = Depends(dependencies.ping_database)
):
    return schemas.HealthCheckResponse(status="ok")