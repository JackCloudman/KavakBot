from fastapi import Depends

from app.dependencies.repositories import get_car_catalog_repository
from app.entities.tool import ToolName
from app.logic.financial_plan_logic import FinancialPlan
from app.repositories.car_catalog.car_catalog_repository_interface import \
    CarCatalogRepositoryInterface
from app.services.tools.tool_service import ToolService
from app.services.tools.tool_service_interface import ToolServiceInterface


def get_tools_service(
        car_repository: CarCatalogRepositoryInterface = Depends(
            get_car_catalog_repository),
) -> ToolServiceInterface:
    # Init ToolService with the tools
    return ToolService({
        ToolName.SEARCH_CAR: car_repository.search,
        ToolName.FINANCIAL_CALCULATOR: FinancialPlan.calculate_financing,
    })
