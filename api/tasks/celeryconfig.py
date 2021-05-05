# from dotenv import load_dotenv
# import os
# load_dotenv()

# class Config():
#     BROKER_USER = os.getenv('BROKER_USER')
#     BROKER_PASS = os.getenv('BROKER_PASS')
#     BROKER_HOST = os.getenv('BROKER_HOST')
#     BROKER_NODE_PORT = os.getenv('BROKER_NODE_PORT')
#     BROKER_VIRTUAL_HOST = os.getenv('BROKER_VIRTUAL_HOST')


# broker_url = (
#     f'amqp://{Config.BROKER_USER}:{Config.BROKER_PASS}@{Config.BROKER_HOST}:'
#     f'{Config.BROKER_NODE_PORT}/{Config.BROKER_VIRTUAL_HOST}'
# )


# task_acks_late = True
# task_store_errors_even_if_ignored = True
# task_default_queue = 'chat_api_tasks'
# task_serializer = 'json'
# accept_content = ['json']
# task_always_eager = False
