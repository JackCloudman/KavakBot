import os
from pathlib import Path
from threading import Lock
from typing import Any, Dict

import typesense
from openai import OpenAI
from redis import Redis

from app.components.cache.cache_interface import CacheInterface
from app.components.cache.redis import AsyncCache
from app.components.configuration.configuration import Configuration
from app.components.configuration.configuration_interface import \
    ConfigurationInterface
from app.components.logger.logger import Logger


class ComponentsMeta(type):
    _instances: Dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Components(metaclass=ComponentsMeta):

    def __init__(self, env: str, config_path: str) -> None:
        self.__env: str = env
        root_dir: str = str(Path(__file__).resolve().parents[2])
        self.__config_path: str = os.path.join(root_dir, config_path)
        self.__components: Dict[str, Any] = self.__bootstrap_components()

    def __bootstrap_components(self) -> Dict[str, Any]:
        if self.__env == 'development':
            return self.__get_dev_components()

        raise ValueError(f'Invalid environment: {self.__env}')

    def __get_dev_components(self) -> Dict[str, Any]:
        configuration: ConfigurationInterface = Configuration(
            self.__env, self.__config_path)

        redis: Redis = Redis(
            configuration.get_configuration('REDIS_HOST', str),
        )

        logger = Logger(
            log_format=configuration.get_configuration('LOG_FORMAT', str),
            log_level=configuration.get_configuration('LOG_LEVEL', str),
        )

        cache: CacheInterface = AsyncCache(
            redis
        )

        typesense_client: typesense.Client = typesense.Client({
            # Must be secret
            'api_key': configuration.get_configuration('TYPESENSE_API_KEY', str),
            'nodes': [{
                'host': configuration.get_configuration('TYPESENSE_HOST', str),
                'port': configuration.get_configuration('TYPESENSE_PORT', int),
                'protocol': configuration.get_configuration('TYPESENSE_PROTOCOL', str),
            }],
            'connection_timeout_seconds': configuration.get_configuration('TYPESENSE_CONNECTION_TIMEOUT_SECONDS', int),
        })

        openai_client: OpenAI = OpenAI()

        return {
            'configuration': configuration,
            'cache': cache,
            'typesense': typesense_client,
            'openai': openai_client,
            'logger': logger,
        }

    def get_component(self, component_name: str) -> Any:
        return self.__components[component_name]
