class Config():
    BROKER_USER = 'guest'
    BROKER_PASS = 'guest'
    BROKER_HOST = '127.0.0.1'
    BROKER_NODE_PORT = 5672
    BROKER_VIRTUAL_HOST = ''


broker_url = (
    f'amqp://{Config.BROKER_USER}:{Config.BROKER_PASS}@{Config.BROKER_HOST}:'
    f'{Config.BROKER_NODE_PORT}/{Config.BROKER_VIRTUAL_HOST}'
)


task_acks_late = True
task_store_errors_even_if_ignored = True
task_default_queue = 'chat_api_tasks'
task_serializer = 'json'
accept_content = ['json']
task_always_eager = False
