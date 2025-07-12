# kafka_producer.py

from confluent_kafka import Producer
import json
import time
import random

# Kafka broker configuration
# Replace 'localhost:9092' with your Kafka broker address if it's different
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'my_test_topic'

def delivery_report(err, msg):
    """
    Callback function to report the delivery status of a message.
    This function is called once for each message produced to indicate
    whether it was successfully delivered or an error occurred.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        # Print details of the successfully delivered message
        print(f"Message delivered to topic '{msg.topic()}' "
              f"[partition {msg.partition()}] @ offset {msg.offset()}")

def produce_messages():
    """
    Produces messages to a Kafka topic.
    """
    # Create a Producer instance
    # The 'bootstrap.servers' configuration points to your Kafka broker(s)
    producer_conf = {
        'bootstrap.servers': KAFKA_BROKER
    }
    producer = Producer(producer_conf)

    print(f"Starting Kafka Producer for topic: {TOPIC_NAME}")
    print(f"Connecting to broker(s): {KAFKA_BROKER}")

    try:
        message_count = 0
        while True:
            # Generate a sample message
            data = {
                'id': message_count,
                'timestamp': time.time(),
                'value': random.randint(1, 1000),
                'message': f"Hello Kafka from Producer {message_count}"
            }
            # Convert the dictionary to a JSON string
            message_value = json.dumps(data)
            # Use a key to ensure messages with the same key go to the same partition
            # For simplicity, we'll use a fixed key here, but it could be dynamic.
            message_key = "test_key"

            # Produce the message asynchronously
            # The delivery_report callback will be invoked upon message delivery or failure.
            producer.produce(
                TOPIC_NAME,
                key=message_key.encode('utf-8'),      # Keys should be bytes
                value=message_value.encode('utf-8'),  # Values should be bytes
                callback=delivery_report
            )

            # Poll the producer to trigger callbacks (delivery reports)
            # This is important for handling asynchronous message delivery.
            producer.poll(0) # Poll with a timeout of 0 to avoid blocking

            print(f"Produced message: {message_value}")
            message_count += 1
            time.sleep(1) # Wait for 1 second before sending the next message

    except KeyboardInterrupt:
        print("\nProducer stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Wait for any outstanding messages to be delivered and delivery reports to be called.
        # This is crucial to ensure all messages are sent before exiting.
        print("Flushing producer messages...")
        producer.flush()
        print("Producer finished.")

if __name__ == "__main__":
    produce_messages()
