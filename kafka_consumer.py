# kafka_consumer.py

from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import sys

# Kafka broker configuration
# Replace 'localhost:9092' with your Kafka broker address if it's different
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'my_test_topic'
# Consumer group ID: all consumers with the same group ID belong to the same consumer group
# This ensures that each message is processed only once by one consumer in the group.
GROUP_ID = 'my_python_consumer_group'

def consume_messages():
    """
    Consumes messages from a Kafka topic.
    """
    # Create a Consumer instance
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest' # Start reading from the beginning of the topic if no offset is committed
    }
    consumer = Consumer(consumer_conf)

    print(f"Starting Kafka Consumer for topic: {TOPIC_NAME}")
    print(f"Belonging to consumer group: {GROUP_ID}")
    print(f"Connecting to broker(s): {KAFKA_BROKER}")

    try:
        # Subscribe to the topic(s)
        consumer.subscribe([TOPIC_NAME])

        while True:
            # Poll for messages with a timeout
            # If no message is available within the timeout, msg will be None.
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                # print("Waiting for message...")
                continue
            if msg.error():
                # Handle Kafka errors
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an error, just means no more messages in this partition for now
                    sys.stderr.write(f"%% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Message successfully received
                # Decode the key and value from bytes to string
                message_key = msg.key().decode('utf-8') if msg.key() else None
                message_value = msg.value().decode('utf-8')

                print(f"Received message: "
                      f"Topic: {msg.topic()}, "
                      f"Partition: {msg.partition()}, "
                      f"Offset: {msg.offset()}, "
                      f"Key: {message_key}, "
                      f"Value: {message_value}")

                try:
                    # Attempt to parse the message value as JSON
                    data = json.loads(message_value)
                    print(f"Parsed Data: {data}")
                except json.JSONDecodeError:
                    print("Message value is not valid JSON.")

    except KeyboardInterrupt:
        print("\nConsumer stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close down the consumer to commit final offsets.
        print("Closing consumer...")
        consumer.close()
        print("Consumer closed.")

if __name__ == "__main__":
    consume_messages()
