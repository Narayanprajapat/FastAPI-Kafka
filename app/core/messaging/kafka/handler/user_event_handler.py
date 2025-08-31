from app.utils.logger import logging
from app.core.messaging.kafka.handler.abstract_handler import Handler


logger = logging.getLogger("kafka.user_event_handler")


class UserEventHandler(Handler):
    def __init__(self):
        super().__init__()

    def execute(self, event_data):
        logger.info("Execute user event handler method")
