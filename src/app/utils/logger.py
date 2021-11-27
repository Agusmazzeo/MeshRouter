import logging
import logging.config
import os


def log_path(filename: str):
    log_dir = os.environ.get("LOG_DIR", ".")
    filename = filename + ".log"
    return os.sep.join((log_dir, filename))


def configure_logger(name: str) -> logging.Logger:
    """Configure the main logger with 3 handlers and formatters.

    This function instances the logger that is supposed to be used as the main logger for the
    component. Subsequent loggers should be instanced with logging.getLogger("<parent_logger>.<child_logger>")

    This method will ensure that child loggers have the same handlers as the main logger while adding 
    traceability and log hierarchy.

    IMPORTANT: Given that workers start from a script contained in queues-manager, the module name needs to be configured
    inside the `config.json` file inside the key "module".

    It has 3 handlers with 3 different formatters:
    - Console (logs everything to console in human-readable format)
    - Main Log File -- Logs everything to a log-file in JSON format with reduced info
    - Error Log File -- Logs only errors to a log file in JSON format

    Arguments
    ---------
    name {str} -- Name of the logger to be configured. This should be the component's name (eg: queues-manager)


    Returns
    -------
    logging.Logger instance with handlers and formatters set up.

    """
    # Setting up formatters
    console_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] >> %(message)s")
    file_formatter = logging.Formatter(
        fmt='{"time":"%(asctime)s", "level": "%(levelname)s", "name":"%(name)s", "msg":"%(message)s"}')
    error_formatter = logging.Formatter(
        fmt='{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", "file": "%(pathname)s",  "line": %(lineno)s, "msg": "%(message)s"}')

    # Setting up handlers
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel("DEBUG")

    file_handler = logging.FileHandler(filename=log_path(
        filename=name), mode="a+", encoding="latin1", delay=None)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel("INFO")

    error_log_handler = logging.FileHandler(filename=log_path(
        filename=f"{name}_error"), mode="a+", encoding="latin1", delay=None)
    error_log_handler.setFormatter(error_formatter)
    error_log_handler.setLevel("WARNING")

    logger = logging.getLogger(name=name)
    logger.setLevel("DEBUG")

    # Adding handlers (with already set up formatters) to instanced logger
    for handler in [console_handler, file_handler, error_log_handler]:
        logger.addHandler(handler)
    return logger


def module_name():
    """Access the config file and return the module name or __name__ if not found."""
    return Config.get_raw().get("module", __name__)
