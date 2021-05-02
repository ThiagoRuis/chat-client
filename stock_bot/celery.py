from celery import Celery, Task
from celery.signals import after_setup_task_logger

from stock_bot import celeryconfig
from stock_bot.broker import init_broker
from stock_bot.consumers import ConsumerStockBot

celery = Celery(worker_hijack_root_logger=False)

# celery.conf.update(application.config)
celery.config_from_object(celeryconfig)
init_broker()

# class ContextTask(Task):
#     def __call__(self, *args, **kwargs):
#         with application.app_context():
#             return self.run(*args, **kwargs)

# celery.Task = ContextTask  # NOQA
celery.steps['consumer'].add(ConsumerStockBot)
