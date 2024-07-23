from kafka import KafkaProducer
import time, os, docker

print("Starting Script")
# Kafka broker address
bootstrap_servers = 'kafka-server:9092'
time.sleep(5) #Waiting for Kafka to fully boot up

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

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


#Has More information
#Everytime MC reboots it zips the log file and we don't get the data about the reboot from the latest.log file
def send_logs_to_kafka(log_message):
    try:
        producer.send('minecraft_new_logs_topic', log_message.encode('utf-8'))
        producer.flush()
    except Exception as e:
        print(f'Error Occured Sending Container Logs to Kafka will retry: {e}')

# Example usage
while True:
    # Fetch Minecraft logs
    minecraft_logs = fetch_minecraft_logs()
    # Send logs to Kafka if logs are available
    if minecraft_logs:
        send_logs_to_kafka(minecraft_logs)
    
    # Simulate interval between log messages
    time.sleep(30)  # Adjust interval as needed

# Close Kafka producer (Note: This won't be reached in the current script as it's in an infinite loop)
producer.close()
