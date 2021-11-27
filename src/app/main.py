from app.utils.logger import configure_logger
from app.services.router import RouterService

def start_app():
    logger = configure_logger("router")
    RouterService(logger=logger)