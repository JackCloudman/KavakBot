from fastapi import Depends

from app.dependencies.repositories import get_car_catalog_repository
from app.entities.tool_name import ToolName
from app.repositories.car_catalog.car_catalog_repository_interface import CarCatalogRepositoryInterface
from app.services.tools.tool_service import ToolService
from app.services.tools.tool_service_interface import ToolServiceInterface


def get_tools_service(
        car_repository: CarCatalogRepositoryInterface = Depends(get_car_catalog_repository),
) -> ToolServiceInterface:
    return ToolService({
        ToolName.SEARCH_CAR: car_repository.search
    })
