from fastapi import Depends
from openai import OpenAI

from app.components.components import Components
from app.components.configuration.configuration import Configuration
from app.dependencies.components import get_components
from app.dependencies.repositories import get_car_catalog_repository
from app.entities.tool import ToolName
from app.logic.financial_plan_logic import FinancialPlan
from app.repositories.car_catalog.car_catalog_repository_interface import \
    CarCatalogRepositoryInterface
from app.services.faq.faq_service import FAQService
from app.services.faq.faq_service_interface import FAQServiceInterface
from app.services.tools.tool_service import ToolService
from app.services.tools.tool_service_interface import ToolServiceInterface


def get_faq_service(
        components: Components = Depends(get_components),
) -> FAQServiceInterface:
    configuration: Configuration = components.get_component('configuration')

    openai_client: OpenAI = components.get_component('openai')

    faq_prompt: str = configuration.get_configuration(
        'FAQ_ASSISTANT_PROMPT', str)
    faq_assistant_id: str = configuration.get_configuration(
        'FAQ_ASSISTANT_ID', str)

    return FAQService(
        instructions=faq_prompt,
        assistant_id=faq_assistant_id,
        openai_client=openai_client,
    )


def get_tools_service(
        car_repository: CarCatalogRepositoryInterface = Depends(
            get_car_catalog_repository),
        faq_service: FAQServiceInterface = Depends(get_faq_service),
) -> ToolServiceInterface:
    # Init ToolService with the tools
    return ToolService({
        ToolName.SEARCH_CAR: car_repository.search,
        ToolName.FINANCIAL_CALCULATOR: FinancialPlan.calculate_financing,
        ToolName.FAQ: faq_service.get_answer,
    })
