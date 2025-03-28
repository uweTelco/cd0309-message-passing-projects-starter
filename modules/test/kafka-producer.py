from kafka import KafkaProducer

def put_report_data(message) :
    TOPIC_NAME = 'udac-counter'
    KAFKA_SERVER = 'localhost:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
    producer.send(TOPIC_NAME, message.encode('utf-8'))
    producer.flush()
    
    
if __name__ == "__main__":
    put_report_data('Hello World')
