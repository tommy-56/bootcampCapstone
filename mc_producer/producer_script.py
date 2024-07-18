from kafka import KafkaProducer
import time, os, docker

print("Starting Script")
# Kafka broker address
bootstrap_servers = 'kafka-server:9092'
time.sleep(5) #Waiting for Kafka to fully boot up

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Function to fetch Minecraft logs from a shared volume
def fetch_minecraft_logs():
    print(os.listdir('/data/logs'))
    # Path to Minecraft logs within the shared volume
    log_file_path = '/minecraft_logs/logs/latest.log'
    
    try:
        with open(log_file_path, 'r') as log_file:
            minecraft_logs = log_file.read()
        return minecraft_logs
    except FileNotFoundError:
        return 'Cant find File'  # Return empty string or handle error accordingly

def fetch_container_logs():
    print("Getting Container Logs")
    container_name = "capstone-minecraft-1"
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

# Function to send logs to Kafka
def send_logs_to_kafka(log_message):
    try:
        producer.send('minecraft_logs_topic', log_message.encode('utf-8'))
        producer.flush()
    except Exception as e:
        print(f'Error Occured Sending Minecraft Logs to Kafka will retry: {e}')

#Has More information
#Everytime MC reboots it zips the log file and we don't get the data about the reboot from the latest.log file
def send_container_logs_to_kafka(log_message):
    try:
        producer.send('docker_logs_topic', log_message.encode('utf-8'))
        producer.flush()
    except Exception as e:
        print(f'Error Occured Sending Container Logs to Kafka will retry: {e}')

# Example usage
while True:
    # Fetch Minecraft logs
    minecraft_logs = fetch_minecraft_logs()
    container_logs = fetch_container_logs()
    # Send logs to Kafka if logs are available
    if minecraft_logs:
        send_logs_to_kafka(minecraft_logs)
    if container_logs:
        send_container_logs_to_kafka(container_logs)
    
    # Simulate interval between log messages
    time.sleep(30)  # Adjust interval as needed

# Close Kafka producer (Note: This won't be reached in the current script as it's in an infinite loop)
producer.close()
