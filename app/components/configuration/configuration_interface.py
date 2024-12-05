from abc import ABC
from typing import Any, Type, TypeVar

ConfigurationType = TypeVar('ConfigurationType')


class ConfigurationInterface(ABC):
    def get_configuration(self,
                          config_name: str,
                          config_type: Type[ConfigurationType],
                          default: Any = None) -> ConfigurationType:
        raise NotImplementedError
