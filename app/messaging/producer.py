import pika
import json
from fastapi.encoders import jsonable_encoder
from app.core.config import settings


class ArenaManagerProducer:
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
                exchange=settings.RABBITMQ_ARENA_MANAGER_EXCHANGE,
                exchange_type='direct',
                durable=True
            )

            self.channel.queue_declare(
                queue=settings.RABBITMQ_ARENA_MANAGER_QUEUE,
                durable=True
            )

            self.channel.queue_bind(
                queue=settings.RABBITMQ_ARENA_MANAGER_QUEUE,
                exchange=settings.RABBITMQ_ARENA_MANAGER_EXCHANGE,
                routing_key=settings.RABBITMQ_ARENA_MANAGER_ROUTING_KEY
            )

    def publish_message(self, message_type: str, data: dict):
        self.connect()

        message = {
            "type": message_type,
            "data": data
        }

        self.channel.basic_publish(
            exchange=settings.RABBITMQ_ARENA_MANAGER_EXCHANGE,
            routing_key=settings.RABBITMQ_ARENA_MANAGER_ROUTING_KEY,
            body=json.dumps(jsonable_encoder(message)),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


producer = ArenaManagerProducer()
