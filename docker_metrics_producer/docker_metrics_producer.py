#Docker Metrics Producer
import docker
from kafka import KafkaProducer
import json
import time

# Initialize Docker client
client = docker.from_env()
time.sleep(10) #Waiting for Kafka to fully boot up
# Kafka broker address
bootstrap_servers = 'kafka-server:9092'

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Function to get container metrics
def get_container_metrics(container_name):
    try:
        container = client.containers.get(container_name)
        stats = container.stats(stream=False)  # Retrieve stats in a non-streaming way
        # Pretty print stats as JSON
        stats_json = json.dumps(stats, indent=2)
        print(stats_json)
        return stats
    except docker.errors.NotFound:
        return None

# Function to send metrics to Kafka
def send_metrics_to_kafka(metrics):
    producer.send('docker_metrics_topic', metrics)
    producer.flush()

# Example usage
container_name = 'capstone-minecraft-1'  # Replace with your container name
while True:
    metrics = get_container_metrics(container_name)
    if metrics:
        send_metrics_to_kafka(metrics)
        print(f"Sent metrics to Kafka: {metrics}")
    else:
        print(f"Container {container_name} not found.")
    
    time.sleep(15)  # Adjust the interval as needed

# Close Kafka producer
producer.close()
