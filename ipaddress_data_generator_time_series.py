import threading
import random
from datetime import datetime, timedelta
import pymongo

# MongoDB connection details
MONGO_URI = "mongodb+srv://"
DB_NAME = "timeseries_db"
PROJECT_COLLECTION_NAME = "gcp_project"
COMPUTE_RESOURCE_COLLECTION_NAME = "gcp_compute_resource_data"

# Number of projects to create
NUM_PROJECTS = 50

# Number of compute resources per project
COMPUTE_RESOURCES_PER_PROJECT = 3

# Number of threads to run concurrently (same as the number of projects)
NUM_THREADS = NUM_PROJECTS

# Number of data points to generate per thread for GCP compute resource
DATA_POINTS_PER_THREAD = COMPUTE_RESOURCES_PER_PROJECT

# Counter to ensure unique strings
string_counter = 0

# Function to generate unique strings
def generate_unique_string(prefix):
    global string_counter
    string_counter += 1
    return f"{prefix}-{string_counter}"

# Function to generate GCP project record
def generate_gcp_project():
    timestamp = datetime.now() + timedelta(seconds=(DATA_POINTS_PER_THREAD))

    return {
            "projectId": generate_unique_string("gcp-project"),
            "projectName": generate_unique_string("GCP Project"),
            "projectNumber": str(random.randint(1000000000, 9999999999)),
            "createTime": datetime.utcnow().isoformat() + "Z",
            "billingInfo": {
                "billingAccountName": generate_unique_string("billing-account"),
                "billingEnabled": True
            },
            "organizationInfo": {
                "organizationId": generate_unique_string("org-id"),
                "organizationName": generate_unique_string("Organization")
            },
            "iamPolicy": {
                "roles": [
                    {
                        "roleName": "roles/viewer",
                        "members": [
                            f"user:{generate_unique_string('example@example.com')}",
                            f"group:{generate_unique_string('example-group@example.com')}",
                            f"serviceAccount:{generate_unique_string('example-service-account@your-project.iam.gserviceaccount.com')}"
                        ]
                    },
                    {
                        "roleName": "roles/editor",
                        "members": [
                            f"user:{generate_unique_string('another-user@example.com')}"
                        ]
                    }
                ]
            },
            "timestamp": timestamp
    }

# Function to insert GCP project records
def insert_gcp_projects():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    project_collection = db[PROJECT_COLLECTION_NAME]

    for _ in range(NUM_PROJECTS):
        project_record = generate_gcp_project()
        project_collection.insert_one(project_record)
        print(f"Inserted GCP project record with projectId: {project_record['projectId']}")

    client.close()

# Function to generate random time-series data for GCP compute resource
def generate_gcp_compute_resource_data(thread_id, project_id):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    compute_resource_collection = db[COMPUTE_RESOURCE_COLLECTION_NAME]

    for _ in range(DATA_POINTS_PER_THREAD):
        timestamp = datetime.now() + timedelta(seconds=(DATA_POINTS_PER_THREAD * thread_id))
        network_interfaces = []

        # Generate multiple network interfaces
        for _ in range(random.randint(1, 3)):
            network_interface = {
                "name": generate_unique_string("network-interface"),
                "ipAddress": f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
                "macAddress": f"{random.randint(0x00, 0xff):02x}:{random.randint(0x00, 0xff):02x}:{random.randint(0x00, 0xff):02x}:{random.randint(0x00, 0xff):02x}",
                # ... (other network interface fields)
            }
            network_interfaces.append(network_interface)

        data_point = {
            "computeResource": {
                "projectId": project_id,
                "instanceName": generate_unique_string("gcp-search-virtualmachine-project"),
                "networkInterfaces": network_interfaces,
                # ... (other fields)
            },
            "timestamp": timestamp
        }

        compute_resource_collection.insert_one(data_point)
        print(f"Thread-{thread_id}: Inserted GCP compute resource data point at {timestamp} for projectId: {project_id}")

    client.close()

# Function to run multiple threads for GCP project and compute resource data generation
def run_threads():
    # Insert GCP project records
    insert_gcp_projects()

    # Retrieve the projectId of the first inserted record
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    project_collection = db[PROJECT_COLLECTION_NAME]
    project_records = project_collection.find().limit(NUM_THREADS)
    project_ids = [record['projectId'] for record in project_records]
    client.close()

    # Insert GCP compute resource data using multiple threads
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=generate_gcp_compute_resource_data, args=(i, project_ids[i]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    run_threads()
    print("GCP project and compute resource data generation completed.")
