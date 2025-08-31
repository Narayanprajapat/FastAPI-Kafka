import json
from app.utils.logger import logging
from confluent_kafka import Producer
from app.core.config.settings import kafka_producer_setting


logger = logging.getLogger(name="kafka.producer")


class KafkaProducer:
    def __init__(self):
        self.producer = Producer(
            {
                "bootstrap.servers": kafka_producer_setting.KAFKA_BROKEN_URL,
                "client.id": kafka_producer_setting.CLIENT_ID,
                "acks": "all",  # Strongest delivery guarantee
            }
        )

    def delivery_report(self, err, msg):
        """Delivery callback for confirming message status."""
        if err is not None:
            logger(f"Delivery failed: {err}")
        else:
            logger(
                f"Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}"
            )

    def produce(self, topic: str, key: str = None, value: dict = None):

        try:
            if not isinstance(value, (dict, list)):
                raise ValueError("Value must be dict or list for JSON serialization")

            # Convert dict/list -> JSON string -> bytes
            json_value = json.dumps(value).encode("utf-8")

            self.producer.produce(
                topic=topic,
                key=key,
                value=json_value,
                callback=self.delivery_report,
            )

            # Ensure delivery_report() is triggered
            self.producer.poll(0)

        except BufferError:
            logger.error(msg="Local producer queue is full, try again later.")
        except Exception as e:
            logger.error(msg=f"Error producing message: {e}")

    def flush(self):
        self.producer.flush()
