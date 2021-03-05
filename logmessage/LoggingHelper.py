import logging
import os
from typing import Dict, Optional, Any, MutableMapping
from opencensus.ext.azure.log_exporter import AzureLogHandler
import azure.functions as func

class CustomLogger(logging.Logger):
    def __init__(self, name: str, prefix: str) -> None:
        LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
        super().__init__(name, level=LOGLEVEL)
        self.prefix = prefix



class LoggingHelper(logging.LoggerAdapter):
    def __init__(self, prefix: str, logger: logging.Logger):
        super(LoggingHelper, self).__init__(logger, {})
        self.prefix = prefix
    # def extra(self, extra: Dict[str, Dict[str, Any]]):
    #     self.extra = extra

    def process(self, msg: str, kwargs: MutableMapping[str, Any]):
        return "[%s] %s" % (self.prefix, msg), kwargs


    def info(self, msg: Any, context: func.Context, properties: Dict[str, str] = None) -> None:

        extra=get_logging_properties({"CorrelationId": "file/one/two/three", "invocationidd": context.invocation_id})
        return super().info(msg, extra=extra)


def get_logger(prefix: str, name: Optional[str] = None) -> LoggingHelper:
    LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
    logging.basicConfig(level=LOGLEVEL)

    if name is not None:
        logger = logging.getLogger(name=name)
    else:
        logger = logging.getLogger()

    try:
        azure_handler = AzureLogHandler()
        logger.addHandler(azure_handler)
    except ValueError as e:
        logger.exception(f"failed to load opencensus AzureLogHandler: {e}", exc_info=e)

    except Exception as e:
        logger.exception(f"failed to load opencensus AzureLogHandler another reason: {e}", exc_info=e)

    logger.setLevel(level=LOGLEVEL)

    log_adapter = LoggingHelper(prefix, logger)
    log_adapter.warn(f"logging set to {LOGLEVEL}")
    return log_adapter


def get_logging_property(k: str, val: str) -> Dict[str, Dict[str, str]]:
    properties = {"custom_dimensions": {k: val}}
    return properties


def get_logging_properties(d: Dict[str, str]):
    properties = {"custom_dimensions": d}
    return properties
