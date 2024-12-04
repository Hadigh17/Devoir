import pika
import json

def handle_payment_created(ch, method, properties, body):
    payment_data = json.loads(body)
    print(f"Accounting Service received payment: {payment_data}")

    accounting_data = {
        'order_id': payment_data['order_id'],
        'payment_status': payment_data['payment_status'],
        'amount': payment_data['payment_amount']
    }

    ch.basic_publish(
        exchange='saga_exchange',
        routing_key='accounting_created',
        body=json.dumps(accounting_data)
    )

    print(f"Accounting record created: {accounting_data}")

def start_listening_for_payment_created():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='saga_exchange', exchange_type='direct')
    channel.queue_declare(queue='accounting_queue')
    channel.queue_bind(exchange='saga_exchange', queue='accounting_queue', routing_key='payment_created')

    channel.basic_consume(queue='accounting_queue', on_message_callback=handle_payment_created, auto_ack=True)

    print('Accounting Service is waiting for payment created events...')
    channel.start_consuming()

if __name__ == "__main__":
    start_listening_for_payment_created()
