#syntheticMetricsScript.py
'''
Purpose: Unit Test Alerting Rules and act as a Back up incase something in the main environment isnt working correctly day of
Simulates a senario where a few important containers are running out of a specfifc resource
Memory for minecraft server since it uses alot and will crash without enough 
Storage for DB's since we cant store anything with out file system space
'''
from prometheus_client import start_http_server, Gauge
import time,random

#Units conversion from bytes to megabytes
byteUnit = 1000000
class GaugeMetrics:
	def __init__(self, name_of_metric, description, container_name):
		self.name_of_metric = name_of_metric
		self.description = description
		self.container_name = container_name
	def create_metric(self):
		newMetric = Gauge(self.name_of_metric, self.description, [self.container_name])
		return newMetric.labels(self.container_name)


def generate_metrics():
	# Create metrics
	cpu_usage = Gauge('syn_cpu_seconds_total', 'Total CPU seconds', ['mode'])
	memory_available = Gauge('syn_memory_MemAvailable_bytes', 'Memory available')
	memory_total_used = Gauge('syn_memory_MemTotalUsage_bytes', 'Total memory Used')

	storage_available = Gauge('syn_fs_available_bytes', 'Total Storage Space Available', ['containerName'])
	storage_used = Gauge('syn_fs_usage_bytes', 'Total Storage Space Used', ['containerName'])
	testing = GaugeMetrics('syn_test_mem', 'testing123', 'really_important_container').create_metric()
	testing.set(1000*byteUnit)
	while True:
		# Simulate high CPU usage
		cpu_usage.labels(mode='idle').set(10)
		
		# Simulate low memory availability
		memory_available.set(100000000)
		
		
		testing.inc(1000*byteUnit)

		memory_total_used.set(random.randint(350,1000)*byteUnit)
		storage_used.labels(containerName='MongoDB').set(random.randint(2000,3000)*byteUnit) # 2GB to 3GB
		time.sleep(30)

def simulate_bad_environment():
	print("Simulating Bad Environment")
	#Set Allocations for each metric
	#cpu_usage.labels(mode='idle').set(10) # change later not sure how it works yet
	#Define Metrics
	mem_avail_mc = GaugeMetrics('syn_memoryAvail_mc', 'Total Available Memory', 'minecraft').create_metric()
	mem_used_mc = GaugeMetrics('syn_memoryUsage_mc', 'Total Used Memory', 'minecraft').create_metric()

	storage_avail_mongo = GaugeMetrics('syn_fsAvailable_mongodb', 'Total Storage Available', 'MongoDB').create_metric()
	storage_used_mongo = GaugeMetrics('syn_fsUsage_mongodb', 'Total Storage Used', 'MongoDB').create_metric()
	storage_avail_sql = GaugeMetrics('syn_fsAvailable_sql', 'Total Storage Available', 'SQL').create_metric()
	storage_used_sql = GaugeMetrics('syn_fsUsage_sql', 'Total Storage Used', 'SQL').create_metric()

	#Set starting usage values
	mem_avail_mc.set(2000*byteUnit) #2GB
	mem_used_mc.set(0) 
	storage_avail_mongo.set(10000*byteUnit) #10GB
	storage_used_mongo.set(9000*byteUnit) # start at 1GB
	storage_avail_sql.set(10000*byteUnit)
	storage_used_sql.set(9000*byteUnit)

	while True: #Simulate resources slowy becoming used over time
		time.sleep(20)
		#Start "Using resources"
		mem_used_mc.inc(500*byteUnit) #increase by 500MB
		storage_used_mongo.inc(500*byteUnit)
		storage_used_sql.inc(500*byteUnit)



if __name__ == '__main__':
	print("Starting Metrics Server")
	# Start up the server to expose the metrics.
	start_http_server(9999)
	#generate_metrics()
	simulate_bad_environment()
