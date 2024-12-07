from fastapi import Depends

from app.components.components import Components
from app.components.configuration.configuration import Configuration
from app.dependencies.components import get_components
from app.repositories.car_catalog.car_catalog_repository import CarCatalogRepository
from app.repositories.car_catalog.car_catalog_repository_interface import CarCatalogRepositoryInterface
from app.repositories.conversation.conversation_repository import ConversationRepository
from app.repositories.conversation.conversation_repository_interface import ConversationRepositoryInterface


def get_conversation_repository(
        components: Components = Depends(get_components)
) -> ConversationRepositoryInterface:
    return ConversationRepository(components.get_component("cache"))


def get_car_catalog_repository(
        components: Components = Depends(get_components)
) -> CarCatalogRepositoryInterface:
    configuration: Configuration = components.get_component("configuration")
    return CarCatalogRepository(
        components.get_component("typesense"),
        configuration.get_configuration("CAR_CATALOG_COLLECTION_NAME", str),
    )
