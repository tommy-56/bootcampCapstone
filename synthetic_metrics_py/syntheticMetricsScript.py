#syntheticMetricsScript.py
from prometheus_client import start_http_server, Gauge
import time,random

class GaugeMetrics:
	def __init__(self, name_of_metric, description, container_name):
		self.name_of_metric = name_of_metric
		self.description = description
		self.container_name = container_name
	def create_metric(self):
		newMetric = Gauge(self.name_of_metric, self.description, [self.container_name])
		return newMetric

# Create metrics
cpu_usage = Gauge('syn_cpu_seconds_total', 'Total CPU seconds', ['mode'])
memory_available = Gauge('syn_memory_MemAvailable_bytes', 'Memory available')
memory_total_used = Gauge('syn_memory_MemTotalUsage_bytes', 'Total memory Used')

storage_available = Gauge('syn_fs_available_bytes', 'Total Storage Space Available', ['containerName'])
storage_used = Gauge('syn_fs_usage_bytes', 'Total Storage Space Used', ['containerName'])

#Units
byteUnit = 1000000
def generate_metrics():
	while True:
		# Simulate high CPU usage
		cpu_usage.labels(mode='idle').set(10)
		
		# Simulate low memory availability
		memory_available.set(100000000)
		
		memory_total_used.set(random.randint(350,1000)*byteUnit)
		storage_used.labels(containerName='MongoDB').set(random.randint(2000,3000)*byteUnit) # 2GB to 3GB
		time.sleep(30)

def simulate_bad_environment():
	#Set Allocations for each metric
	cpu_usage.labels(mode='idle').set(10) # change later not sure how it works yet
	memory_available.set(2000*byteUnit) #2GB
	storage_available.labels(containerName='MongoDB').set(10000*byteUnit) #10GB
	#Set starting usage values
	memory_total_used.set(random.randint(500,1000)*byteUnit) # Use between 500MB and 1GB
	storage_used.labels(containerName='MongoDB').set(random.randint(2000,3000)*byteUnit) # 2GB to 3GB
	while True:
		time.sleep(20)
		#Start "Using resources"
		memory_total_used.inc(100*byteUnit)
		storage_used.labels(containerName='MongoDB').inc(500*byteUnit)



if __name__ == '__main__':
	print("Starting Metrics Server")
	print(cpu_usage)
	# Start up the server to expose the metrics.
	start_http_server(9999)
	generate_metrics()
	#simulate_bad_environment()
