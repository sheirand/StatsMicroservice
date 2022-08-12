import pika
import json
from aio_pika import connect_robust
import logging
from core.settings import (PUBLISH_QUEUE, RABBIT_PW, RABBIT_USER,
                           RABBIT_CONNECTION, RABBIT_PORT)


logger = logging.getLogger(__name__)


class PikaClient:

    def __init__(self, process_callable):
        self.publish_queue_name = PUBLISH_QUEUE
        self.credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PW)
        self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBIT_CONNECTION,
                                          port=RABBIT_PORT,
                                          credentials=self.credentials,
                                          heartbeat=600,
                                          blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable
        logger.info('Pika connection initialized')

    async def consume(self, loop):
        print('consume')
        """Setup message listener with the current running loop"""
        connection = await connect_robust(host=RABBIT_CONNECTION,
                                          port=RABBIT_PORT,
                                          login=RABBIT_USER,
                                          password=RABBIT_PW,
                                          loop=loop)
        print("robust connection")
        channel = await connection.channel()
        queue = await channel.declare_queue(PUBLISH_QUEUE)
        await queue.consume(self.process_incoming_message, no_ack=False)
        await queue.purge()
        logger.info('Established pika async listener')
        return connection

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        await message.ack()
        body = message.body
        print("process_incoming messages")
        logger.info('Received message')
        if body:
            self.process_callable(json.loads(body))
