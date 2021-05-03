from typing import Iterable

from celery import chain
from celery.bootsteps import ConsumerStep
from celery.utils.log import get_task_logger
from kombu import Consumer, Message

from broker import BrokerConnEnum
from utils import ConsumerMixin
from tasks import get_stock_info

logger = get_task_logger('stock_bot')


class ConsumerStockBot(ConsumerStep, ConsumerMixin):
    def get_consumers(self, channel) -> Iterable[Consumer]:
        return self._get_consumers(
            self._get_queue(
                BrokerConnEnum.STOCK_BOT_INFO), channel, (self.handle_message,)
        )

    def handle_message(self, body, message: Message):
        self._handle_message(message, BrokerConnEnum.STOCK_BOT_INFO, chain(
            get_stock_info.s(body),
        ))
        message.ack()
