import azure.functions as func
import datetime
from .LoggingHelper import get_logger

logger = get_logger("breathe.fn_logmessage")


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:

    logger.info(f"HTTP trigger - no correlation ID {context.invocation_id}", context)

    logger.info(f"HTTP trigger - correlation id {context.invocation_id}", context, "/zip/file/here")

    logger.info(f"HTTP Trigger with additiona properties {context.invocation_id}", context, "filezip....json", record={"foo": "bar", "one": "two"})

    # logger.info('Python HTTP trigger function processed a request.', extra=get_logging_properties({"CorrelationId": "file/one/two/three", "invocationidd": context.invocation_id}))
    # root_logger.info("[breathe] - from root logger", extra=get_logging_properties({"CorrelationId": "file/one/two/three", "invocationidd": context.invocation_id}))

    # logger.debug(f"this is a debug message with id: {context.invocation_id}")
    # logger.warn(f"this is a Warn message {context.invocation_id}")
    # logger.error(f"this is a Error message {context.invocation_id}")
    # logger.exception(f"this is a Exception Message message {context.invocation_id}") # , Exception("an exception example"))

    message = req.params.get("message")
    if not message:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            message = req_body.get("message")

    if message:
        return func.HttpResponse(f"Your message -- at {datetime.datetime.now()} - {message}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a message in the query string or in the request body for a personalized response.",
            status_code=200,
        )
