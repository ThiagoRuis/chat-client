from celery import Celery, Task
from celery.signals import after_setup_task_logger

from tasks import celeryconfig
from tasks.broker import init_broker
from tasks.consumers import ConsumerChatAPI

celery = Celery(worker_hijack_root_logger=False)

celery.config_from_object(celeryconfig)
init_broker()

celery.steps['consumer'].add(ConsumerChatAPI)
