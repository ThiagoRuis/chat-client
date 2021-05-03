from dotenv import load_dotenv
import os
import json
import signal
import socket
from contextlib import contextmanager

from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from kombu.exceptions import ConnectionError, HttpError, OperationalError
from mongoengine import connect

from tasks.celeryconfig import Config
from models import Message

load_dotenv()
logger = get_task_logger('chat_api')

connect(os.getenv('APP_DATABASE'), username=os.getenv('APP_MONGO_USER'),
        password=os.getenv('APP_MONGO_PASS'), authentication_source='admin')

CeleryStockBot = Celery(
    'stock_bot',
    broker=f'amqp://{Config.BROKER_USER}:{Config.BROKER_PASS}@{Config.BROKER_HOST}:'
    f'{Config.BROKER_NODE_PORT}/{Config.BROKER_VIRTUAL_HOST}',
)


def send_to_stock_bot(data: dict, task: str, queue: str):
    try:
        CeleryStockBot.send_task(task, queue=queue, kwargs=data)
    except Exception as err:
        logger.exception(f'Unexpected Error: {err}')
        raise err

@shared_task(
    name='get_stock_info',
    default_retry_delay=5,
    max_retries=1800 // 5,
    ignore_result=True,
    autoretry_for=(ConnectionError, HttpError,
                   OperationalError, ConnectionRefusedError, socket.error),
)
def get_stock_info(stock_code: str):
    try:
        send_to_stock_bot({
            'stock_code': stock_code
        },
            task='stock_bot.get_stock_info',
            queue='stock_bot_info'
        )
        logger.info(f'Sent get_stock_info to StockBot: {stock_code}')
    except Exception as err:
        logger.exception(f'Unexpected Error: {err}')


@shared_task(
    name='register_stock_info',
    default_retry_delay=5,
    max_retries=1800 // 5,
    ignore_result=True,
    autoretry_for=(ConnectionError, HttpError,
                   OperationalError, ConnectionRefusedError, socket.error),
)
def register_stock_info(body):
    try:
        stock = json.loads(body[1].get('stock'))
        content = f'{stock.get("Symbol")} quote is ${stock.get("Close")} per share'
        msg = Message(text=content).save()
        logger.info(f'Registering StockBot reply on message document {msg}')
    except Exception as err:
        logger.exception(f'Unexpected Error: {err}')
