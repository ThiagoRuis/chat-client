from collections import namedtuple
from typing import Iterable

from kombu import Connection, Exchange, Queue

from celeryconfig import broker_url


def conn() -> Connection:
    return Connection(broker_url)


class ListStatesEnumMixin:
    @classmethod
    def all_states(cls) -> Iterable:
        return tuple(
            [getattr(cls, name) for name in dir(cls) if not name.startswith(
                '__') and not callable(getattr(cls, name))]
        )


class ExchangeEnum(ListStatesEnumMixin):
    STOCK_BOT_EXCHANGE = 'stock_bot'


class QueueEnum(ListStatesEnumMixin):
    STOCK_BOT_INFO = 'stock_bot_info'


class RoutingKeyEnum(ListStatesEnumMixin):
    STOCK_BOT_INFO = f'{ExchangeEnum.STOCK_BOT_EXCHANGE}.read'


BrokerResources = namedtuple(
    'BrokerResources', ['exchange', 'queue', 'routing_key'])


class BrokerConnEnum(ListStatesEnumMixin):
    STOCK_BOT_INFO = BrokerResources(
        ExchangeEnum.STOCK_BOT_EXCHANGE,
        QueueEnum.STOCK_BOT_INFO,
        RoutingKeyEnum.STOCK_BOT_INFO
    )


def init_broker():
    channel = conn().channel()
    for item in BrokerConnEnum.all_states():
        exchange = None
        if item.exchange:
            exchange = Exchange(channel=channel, name=item.exchange,
                                type='topic', durable=True, auto_delete=False)

        Queue(
            channel=channel, name=item.queue, durable=True, exchange=exchange, routing_key=item.routing_key
        ).declare()
