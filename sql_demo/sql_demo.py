import mysql.connector
import time

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


# The name of the table you want to check
table_name = 'Logs'

# SQL query to count the number of rows in the table
query = f"SELECT COUNT(*) FROM {table_name}"

sql_has_entries = False

# Execute the query
mysql_cursor.execute(query)

# Fetch the result
result = mysql_cursor.fetchone()

while result is None or result[0] == 0:
    print("No entries yet... trying again!")
    result = mysql_cursor.fetchone()
    time.sleep(5)


query = f"SELECT * FROM `{table_name}` WHERE `LogLevel` = 'main/ERROR'"

mysql_cursor.execute(query)

result = mysql_cursor.fetchall()

for x in result:
    print(x)

mysql_connection.close()
mysql_cursor.close()