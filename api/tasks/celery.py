from celery import Celery, Task
from celery.signals import after_setup_task_logger

from api.tasks import celeryconfig
from api.tasks.broker import init_broker
from api.tasks.consumers import ConsumerChatAPI

celery = Celery(worker_hijack_root_logger=False)

celery.config_from_object(celeryconfig)
init_broker()

celery.steps['consumer'].add(ConsumerChatAPI)
