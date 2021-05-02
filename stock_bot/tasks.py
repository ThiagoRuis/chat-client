import json
import signal
import socket
from contextlib import contextmanager

from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from kombu.exceptions import ConnectionError, HttpError, OperationalError

from stock_bot.celeryconfig import Config
from stock_bot.services import stock_info

logger = get_task_logger('stock_bot')


CeleryChatAPI = Celery(
    'chat_api',
    broker=f'amqp://{Config.BROKER_USER}:{Config.BROKER_PASS}@{Config.BROKER_HOST}:'
    f'{Config.BROKER_NODE_PORT}/{Config.BROKER_VIRTUAL_HOST}',
)


@contextmanager
def timeout(time):
    def raise_timeout(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(time)

    try:
        yield
    except TimeoutError:
        pass
    finally:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def send_to_chat_api(data: dict, task: str, queue: str):
    with timeout(5):
        try:
            CeleryChatAPI.send_task(task, queue=queue, kwargs=data)
        except Exception as err:
            logger.exception(f'Unexpected Error: {err}')
            raise err


@shared_task(
    name='get_stock_info',
    default_retry_delay=5,
    max_retries=1800 // 5,
    ignore_result=True,
    autoretry_for=(ConnectionError, TimeoutError, HttpError,
                   OperationalError, ConnectionRefusedError, socket.error),
)
def get_stock_info(stock_code: str):
    try:
        info = stock_info(stock_code)

        send_to_chat_api({
            'stock': json.dumps(info)
        },
            task='chat_api.get_stock_info',
            queue='chat_api'
        )
        logger.info(f'Sent stock info to ChatAPI: {stock_code}')
    except Exception as err:
        logger.exception(f'Unexpected Error: {err}')
