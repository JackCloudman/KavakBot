import os

from app.components.components import Components


def get_components() -> Components:
    env: str = os.getenv('ENV', 'development')
    config_path: str = os.getenv('CONFIG_PATH', 'configuration')
    return Components(
        env=env,
        config_path=config_path,
    )
