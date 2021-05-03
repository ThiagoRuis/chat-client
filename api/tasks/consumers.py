from typing import Iterable

from celery import chain
from celery.bootsteps import ConsumerStep
from celery.utils.log import get_task_logger
from kombu import Consumer, Message

from tasks.broker import BrokerConnEnum
from tasks.utils import ConsumerMixin
from tasks.tasks import register_stock_info

logger = get_task_logger('chat_api')


class ConsumerChatAPI(ConsumerStep, ConsumerMixin):
    def get_consumers(self, channel) -> Iterable[Consumer]:
        return self._get_consumers(
            self._get_queue(
                BrokerConnEnum.STOCK_BOT_REPLY), channel, (self.handle_message,)
        )

    def handle_message(self, body, message: Message):
        self._handle_message(message, BrokerConnEnum.STOCK_BOT_REPLY, chain(
            register_stock_info.s(body),
        ))
        message.ack()
