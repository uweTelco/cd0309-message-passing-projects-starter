from kafka import KafkaConsumer
import logging

def consume_kafka_messages():
    """
    Consumes messages from the 'udac_counter' Kafka topic
    Prints received messages to console
    """
    try:
        # Set up consumer with same config as producer
        consumer = KafkaConsumer(
            'udac-counter',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',  # Start from beginning of topic
            group_id='test-group',
            api_version=(2, 8, 1)
        )

        print("Listening for messages on 'udac_counter' topic...")
        for message in consumer:
            print(f"\nReceived message:")
            print(f"Topic: {message.topic}")
            print(f"Partition: {message.partition}")
            print(f"Offset: {message.offset}")
            print(f"Value: {message.value.decode('utf-8')}")
            print("---------------------------")

    except Exception as e:
        print(f"Error consuming messages: {str(e)}")
        logging.error("Kafka Consumer Error", exc_info=True)

if __name__ == "__main__":
    consume_kafka_messages()
