import pika
import json
from app.core.config import settings


class RabbitMQProducer:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(settings.RABBITMQ_URL)
            )
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange=settings.RABBITMQ_EXCHANGE,
                exchange_type='direct',
                durable=True
            )

    def publish_message(self, message_type: str, data: dict):
        self.connect()
        message = {
            "type": message_type,
            "data": data
        }
        self.channel.basic_publish(
            exchange=settings.RABBITMQ_EXCHANGE,
            routing_key="arena_manager",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


producer = RabbitMQProducer()
