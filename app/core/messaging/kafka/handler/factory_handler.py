from app.utils.logger import logging
from app.core.config.enums import EventsName
from app.core.messaging.kafka.handler.abstract_handler import Handler
from app.core.messaging.kafka.handler.user_event_handler import UserEventHandler

logger = logging.getLogger(name='kafka.factory_handler')

class FactoryHandler:
    _handlers = {}
    @staticmethod
    def init_handlers()->None:
        FactoryHandler._handlers = {
            EventsName.USER_EVENTS.value: UserEventHandler()
        }
    
    @staticmethod
    def get_instance(event_name: str)-> Handler:
        if event_name not in FactoryHandler._handlers:
            FactoryHandler.init_handlers()
            
        return FactoryHandler._handlers[event_name]