from kafka import KafkaConsumer
from pymongo import MongoClient
from kafka.errors import NoBrokersAvailable
import mysql.connector
import re
import time

# Kafka and MongoDB configuration as well as MySQL

kafka_topic = 'minecraft_new_logs_topic'
kafka_bootstrap_servers = ['kafka-server:9092']
mongo_connection_string = 'mongodb://mongo1:27017/'
mongo_db_name = 'minecraft_db'
mongo_collection_name = 'minecraft_collection'

#Make the sql connection
mysql_connection = mysql.connector.connect(user='root', password='root', host='mysql', port="3306", database='db')
mysql_cursor = mysql_connection.cursor()
print("DB connected")

# Create Kafka consumer
kafka_healthy = False

while kafka_healthy == False:
    try:
        consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers=kafka_bootstrap_servers,
            value_deserializer=lambda m: m.decode('utf-8')
        )
        kafka_healthy = True
    except NoBrokersAvailable as e:
            print(f"Error: {e}")
            time.sleep(5)

try:
    # Create MongoDB client
    mongo_client = MongoClient(mongo_connection_string)
    db = mongo_client[mongo_db_name]
    collection = db[mongo_collection_name]
except Exception as e:
    print(e)

# Regex pattern to parse log entries
log_pattern = re.compile(
    r'\[(?P<TimestampServer>\d{2}:\d{2}:\d{2})\] '
    r'\[(?P<LogLevel>[^\]]+)\] '
    r'\[(?P<Source>[^\]]+/)\]: '
    r'(?P<Message>.+)'
)
# Consume messages from Kafka and insert into MongoDB
for message in consumer:
    print("Looking at messages")
    message_lines = message.value.split("\n")
    for line in message_lines:
        match = log_pattern.search(line)
        if match:
            sql_insert_query = """
            INSERT INTO Logs (_id, TimestampServer, LogLevel, Source, Message)
            VALUES (%s, %s, %s, %s, %s)
            """

            collection.insert_one(match.groupdict())
            #Getting the id of the last inserted document
            mongo_document = collection.find({}).sort({_id:-1}).limit(1)
            values = (
                str(mongo_document["_id"]),
                mongo_document["TimestampServer"],
                mongo_document["LogLevel"],
                mongo_document["Source"],
                mongo_document["Message"]
            )
            mysql_cursor.execute(sql_insert_query, values)
            mysql_connection.commit()
    break

# Close the MongoDB client
mongo_client.close()