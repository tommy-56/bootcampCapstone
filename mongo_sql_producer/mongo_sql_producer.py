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

# Create Kafka consumer
kafka_healthy = False
sql_healthy = False

while sql_healthy == False:
    try:
        mysql_connection = mysql.connector.connect(user='root', password='root', host='mysql', port="3306", database='db')
        mysql_cursor = mysql_connection.cursor()
        print("DB connected")
        sql_healthy = True
    except:
        print("Connection Error... retrying")
        time.sleep(5)


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
            matchdict = match.groupdict()
            _id = collection.insert_one(matchdict)

            values = (
                str(_id.inserted_id),
                matchdict["TimestampServer"],
                matchdict["LogLevel"],
                matchdict["Source"],
                matchdict["Message"]
            )
            mysql_cursor.execute(sql_insert_query, values)
 
    break
mysql_connection.commit()

mysql_cursor.execute("SELECT * FROM Logs")

myresult = mysql_cursor.fetchall()

for x in myresult:
  print(x)


# Close the MongoDB client
mongo_client.close()