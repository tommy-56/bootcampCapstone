from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import time, os, docker
import mongo_sql_producer

#Get logs from the minecraft container
def fetch_minecraft_logs():
    print("Getting Container Logs")
    container_name = "bootcampcapstone-minecraft-1"
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        logs = container.logs().decode('utf-8')
        print(logs)
        return logs
    except docker.errors.NotFound:
        print(f"Container '{container_name}' not found.")
        return f"Container '{container_name}' not found."
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"


# Via the Kafka Producer send logs to kafka topic
def send_logs_to_kafka(log_message):
    var = mongo_sql_producer.MongoProducer()
    var.insert_to_mongo(log_message)
    try:
        producer.send('minecraft_new_logs_topic', log_message.encode('utf-8'))
        producer.flush()
    except Exception as e:
        print(f'Error Occured Sending Container Logs to Kafka will retry: {e}')



if __name__ == '__main__':
    print("Starting Script")
    kafka_healthy = False
    while kafka_healthy == False:
        try:
            # Kafka broker address
            bootstrap_servers = 'kafka-server:9092'
            # Initialize Kafka producer
            producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
            kafka_healthy = True
        except NoBrokersAvailable as e:
            print(f"Error: {e}")
            time.sleep(5)
    
    while True:
        print("Fetching Logs")
        # Fetch Minecraft logs
        minecraft_logs = fetch_minecraft_logs()
        # Send logs to Kafka if logs are available
        if minecraft_logs:
            send_logs_to_kafka(minecraft_logs)
        
        # Send Updates on an interval to keep kafka updated
        time.sleep(30)  # Adjust interval as needed

