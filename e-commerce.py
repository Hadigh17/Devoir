import pika
import json

def start_order_creation():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='saga_exchange', exchange_type='direct')

    order_data = {
        'order_id': '69',
        'user_id': 'Rami',
        'total_amount': 2123
    }

    channel.basic_publish(
        exchange='saga_exchange',
        routing_key='order_created',
        body=json.dumps(order_data)
    )

    print(f"Order created and event sent: {order_data}")
    connection.close()

if __name__ == "__main__":
    start_order_creation()
