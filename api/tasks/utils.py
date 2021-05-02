from typing import Callable, Iterable

from celery.canvas import Signature
from celery.utils.log import get_task_logger
from kombu import Consumer, Exchange, Message, Queue

from api.tasks.broker import BrokerResources, BrokerConnEnum

logger = get_task_logger('chat_api')


class ConsumerMixin:
    @staticmethod
    def _get_consumers(queue: Queue, channel, callbacks: Iterable[Callable]) -> Iterable[Consumer]:
        return Consumer(channel, queues=[queue], callbacks=callbacks, accept=['json']),

    @staticmethod
    def _handle_message(message: Message, broker_resource: BrokerResources, tasks: Signature):
        logger.info(
            f'A message with the delivery tag {message.delivery_tag} came from {broker_resource.queue} with body '
            f'{message.body}'
        )
        task_id = tasks()
        logger.info(f'Tasks called with id {task_id}')

    @staticmethod
    def _get_queue(broker_conn_enum: BrokerConnEnum) -> Queue:
        return Queue(
            broker_conn_enum.queue,
            Exchange(broker_conn_enum.exchange, type='topic'),
            broker_conn_enum.routing_key
        )
