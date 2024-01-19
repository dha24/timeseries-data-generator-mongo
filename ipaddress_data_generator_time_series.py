import threading
import random
from datetime import datetime, timedelta
import pymongo

# MongoDB connection details
MONGO_URI = "mongodb+srv://user:pass@cluster0.z63ug.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "timeseries_db"
COLLECTION_NAME = "gcp_compute_resource_data"

# Number of threads to run concurrently
NUM_THREADS = 2

# Number of data points to generate per thread
DATA_POINTS_PER_THREAD = 100

# Function to generate random time-series data for GCP compute resource
def generate_gcp_compute_resource_data(thread_id):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    for _ in range(DATA_POINTS_PER_THREAD):
        timestamp = datetime.now() + timedelta(seconds=(DATA_POINTS_PER_THREAD * thread_id))
        data_point = {
                "instanceName": f"instance-{random.randint(1, 10)}",
                "machineType": random.choice(["n1-standard-2", "n1-standard-4"]),
                "zone": random.choice(["us-central1-a", "us-east1-b"]),
                "network": {
                    "networkName": f"network-{random.randint(1, 5)}",
                    "subnetwork": f"subnet-{random.randint(1, 5)}",
                    "externalIP": random.choice(["static", "ephemeral"]),
                    "tags": ["web", "dev"]
                },
                "disk": {
                    "diskName": f"disk-{random.randint(1, 3)}",
                    "sizeGB": random.randint(50, 200),
                    "type": random.choice(["pd-ssd", "pd-standard"])
                },
                "privateIP": f"10.0.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "publicIP": f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "dnsName": f"instance-{random.randint(1, 10)}.domain.com",
                "metadata": {
                    "project": f"project-{random.randint(1, 3)}",
                    "user": f"user-{random.randint(1, 5)}"
                },
             "timestamp": timestamp.isoformat()
            },

        collection.insert_one(data_point)
        print(f"Thread-{thread_id}: Inserted GCP compute resource data point at {timestamp}")

    client.close()

# Function to run multiple threads for GCP compute resource data generation
def run_threads():
    threads = []

    for i in range(NUM_THREADS):
        thread = threading.Thread(target=generate_gcp_compute_resource_data, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    run_threads()
    print("GCP compute resource data generation completed.")
