import json
import asyncio
from typing import List
from confluent_kafka import Consumer
from app.utils.logger import logging
from app.core.config.enums import EventsName
from app.core.config.settings import kafka_consumer_setting
from app.core.messaging.kafka.handler.factory_handler import FactoryHandler

logger = logging.getLogger(name="kafka.consumer")


class KafkaConsumer:
    def __init__(self, topics: list) -> None:
        self.consumer = Consumer(
            {
                "bootstrap.servers": kafka_consumer_setting.KAFKA_BROKEN_URL,
                "group.id": kafka_consumer_setting.KAFKA_GROUP_ID,
                "auto.offset.reset": "earliest",
            }
        )

        self.running = False
        self.topics = topics

    def start(self):
        self.consumer.subscribe(self.topics)
        logger.info(f"Subscribe to topics: {self.topics}")

        self.running = True

        batch_size = 1000
        timeout = 300
        try:
            while self.running:
                batch_msg = self.consumer.consume(batch_size, timeout=timeout)
                if not batch_msg:
                    continue

                messages = []

                for msg in batch_msg:
                    if msg.error():
                        logger.info(f"Consumer error: {msg.error()}")
                        continue

                    message = json.loads(msg.value().decode("utf-8"))
                    messages.append(message)

                logger.info("-----Messages Received-----")
                if messages:
                    self.consumer_handler(messages=messages)

        except Exception as e:
            logger.error(f"Error consuming message: {e}")
        finally:
            self.close()

    def consumer_handler(self, messages: List[dict]) -> None:
        event_groups = {}

        for event in messages:
            event_name = event.get("eventName")
            if event_name not in event_groups:
                event_groups[event_name] = []

            event_groups[event_name].append(event.get("eventData", {}))

        for event_name, event_data in event_groups.items():
            try:
                if event_name in EventsName.ALL_EVENTS.value():
                    handler = FactoryHandler.get_instance(event_name=event_name)
                    handler.execute()
            except Exception as e:
                logger.error(
                    msg={
                        "message": f"Getting exception while executing method --{event_name}",
                        "error": str(e),
                    }
                )

    def close(self):
        logger.info("Closing kafka consumer...")
        self.consumer.close()
        self.running = False


async def consume_messages():
    """Run Kafka consumer in a separate thread."""
    loop = asyncio.get_running_loop()

    kafka_consumer = loop.run_in_executor(
        None, lambda: KafkaConsumer(topics=[kafka_consumer_setting.KAFKA_TOPIC]).start()
    )

    await asyncio.gather(kafka_consumer)
