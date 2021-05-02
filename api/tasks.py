from kombu import Connection


class StockInfoProducer():
    connection = Connection('amqp://guest:guest@localhost:5672//')
    producer = connection.Producer()

    def register(stock_data):
        producer.publish(
            stock_data,
            exchange='',
            routing_key='hipri.add'
        )
