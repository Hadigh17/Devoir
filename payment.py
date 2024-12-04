import pika
import json

def handle_order_created(ch, method, properties, body):
    order_data = json.loads(body)
    print(f"Payment Service received order: {order_data}")

    payment_data = {
        'order_id': order_data['order_id'],
        'payment_status': 'processed',
        'payment_amount': order_data['total_amount']
    }

    ch.basic_publish(
        exchange='saga_exchange',
        routing_key='payment_created',
        body=json.dumps(payment_data)
    )

    print(f"Payment created: {payment_data}")

def start_listening_for_order_created():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='saga_exchange', exchange_type='direct')
    channel.queue_declare(queue='payment_queue')
    channel.queue_bind(exchange='saga_exchange', queue='payment_queue', routing_key='order_created')

    channel.basic_consume(queue='payment_queue', on_message_callback=handle_order_created, auto_ack=True)

    print('Payment Service is waiting for order creation events...')
    channel.start_consuming()

if __name__ == "__main__":
    start_listening_for_order_created()
