# Real Time Minecraft Server Log Processing and System Analysis

## To run
docker compose up --build -d

## To stop
docker compose down

## Project Description
In modern gaming environments, server management and performance monitoring are critical for delivering a seamless user experience. This capstone project focused on the development of an advanced log management and analysis system for a Minecraft server. By leveraging cutting-edge technologies such as Apache Kafka, MySQL, MongoDB, Prometheus, and Grafana, the project aimed to enhance the ability to collect, store, analyze, and visualize server logs to improve server performance and reliability. Minecraft servers generate vast amounts of log data that are essential for monitoring server health, diagnosing issues, and ensuring a positive gaming experience for users

## Component List

The following is a list and explanation of the technologies running in our project. Each of these components is running in a docker container within a docker compose project. 

### Main Server
Minecraft Server
Purpose: To have a live server and application running to produce real time logs and system information rather than developing a fully synthetic application. 

### Data Management
Kafka
- Purpose: Serving as the message queue for log messages from the minecraft server. 
- Usage: A python producer script pushes log information in real time from the minecraft container and into a Kafka Topic. Using an exporter for Kafka the data in the topic is then sent to MongoDB
- Available on: http://localhost:9092

MongoDB
- Purpose: To ingest server logs from Kafka and store the raw data in a series of documents.
- Usage: Via an exporter for Kafka data from a topic is pushed into a mongoDB collection and stored for later use.
- Available on: http://localhost:27017 

SQL
- Purpose: To store processed log information from MongoDB in a relational manner, creating a summary of the data
- Usage: Via a pymongo script raw log data stored in documents in Mongo is formatted to be stored in SQL. 

### System Monitoring

cAdvisor
- Purpose: To expose system metrics from all the containers in the environment. Tracks various performance metrics of all the containers (CPU/ Memory usage…)
- Usage: Used by Prometheus to gather system performance data exposed by the cAdvisor container
- Available on: http://localhost:8080

Prometheus
- Purpose: To collect metrics exposed by cAdvisor and the Minecraft application in a queryable format for use in other components. Also to manage alerts for containers.
- Usage: Used by Grafana to gather information to visualize. Also used to configure and send alerts about issues with container behavior.
- Available on: http://localhost:9090

AlertManager
- Purpose: To send alerts to a discord webhook when Prometheus rules detect there is an issue with the system.
- Usage: Shows alerts that are currently firing. If there is an issue with discord, if you can see the alerts in the alert manager then that means they fired properly.
- Available on: http://localhost:9093

Grafana
- Purpose: To visualize all monitoring aspects of the system.
- Usage: Queries Prometheus to display system information in Time Series Format. You can log in and explore the dashboards. 
- Available on: http://localhost:3000

## Troubleshooting

### My dashboards are not populated with any information

The reason for this could be because you have not logged into the Minecraft server. The Minecraft Server Stats dashboard is dependent on the stats that the Minecraft server generates. Possible stats that could be affected are the players online, chunks, server tick time, etc. For the Metrics dashboard, as long as the containers are up and running, the data should be getting populated. 

### My Docker Desktop is freezing up, and not fully loading the Minecraft server

Originally when developing this capstone project, we began by developing on our Desktop PC’s which are more suited to running Minecraft with Mods. Modded Minecraft can be a bit resource intensive depending on the type of mods you are running, and the hardware you are running it on. The main issue is memory. Minecraft recommends 8g’s for the mods, but we have gotten away with doing anywhere from 2g's to 4 g’s without doing anything too intensive on the actual server. Due to this, you may have to do some trouble shooting inside of the docker-compose.yml file in the project directory. In the memory section, just update the number and experiment with what works best for you. 

