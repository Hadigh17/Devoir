import pika
import json

def handle_accounting_created(ch, method, properties, body):
    accounting_data = json.loads(body)
    print(f"Inventory Service received accounting data: {accounting_data}")

    inventory_data = {
        'order_id': accounting_data['order_id'],
        'status': 'inventory_updated',
        'amount': accounting_data['amount']
    }

    print(f"Inventory updated for order {inventory_data['order_id']}")

def start_listening_for_accounting_created():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='saga_exchange', exchange_type='direct')
    channel.queue_declare(queue='inventory_queue')
    channel.queue_bind(exchange='saga_exchange', queue='inventory_queue', routing_key='accounting_created')

    channel.basic_consume(queue='inventory_queue', on_message_callback=handle_accounting_created, auto_ack=True)

    print('Inventory Service is waiting for accounting created events...')
    channel.start_consuming()

if __name__ == "__main__":
    start_listening_for_accounting_created()
