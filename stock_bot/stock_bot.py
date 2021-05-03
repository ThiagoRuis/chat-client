from celery import Celery, Task
from celery.signals import after_setup_task_logger

import celeryconfig
from broker import init_broker
from consumers import ConsumerStockBot

celery = Celery(worker_hijack_root_logger=False)
celery.config_from_object(celeryconfig)
init_broker()

celery.steps['consumer'].add(ConsumerStockBot)
