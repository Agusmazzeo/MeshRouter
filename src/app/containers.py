from dependency_injector import containers, providers

from app.utils.logger import configure_logger
from config.classes import Config

logger = configure_logger("tpo")

class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    config = providers.Configuration()
        
    logger = providers.Object(logger)
