from faker import Faker
from faker.providers import BaseProvider
from decimal import Decimal
from datetime import datetime, timedelta
import random
import pymongo

fake = Faker()

# Custom Provider for location data
class LocationProvider(BaseProvider):
    def location(self):
        return {
            "type": "Point",
            "coordinates": [float(fake.longitude()), float(fake.latitude())]
        }

fake.add_provider(LocationProvider)

# Function to generate and ingest random data into MongoDB
def generate_and_ingest_data(duration_days=1, granularity=3600, granularity_unit='hour'):
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://XXXX")
    db = client["tsDb"]
    collection = db["weather_info_min"]

    current_date = datetime.now()

    for _ in range(duration_days):
        for _ in range(24 * 60 * 60 // granularity):
            timestamp = current_date + timedelta(microseconds=random.randint(0, 999999))

            data_point = {
                "metadata": {
                    "sensorId": fake.random_int(min=5000, max=5010),
                    # "type": fake.random_element(elements=('omni', 'other_type', 'SensorTech_Solutions', 'PrecisionSense_Innovations', 'QuantumSensors_Inc', 'AccuSense_Technologies', 'SensorCraft_Dynamics', 'OptiSense_Systems', 'SmartSense_Innovations', 'OmniSensors_Ltd', 'InteliSense_Technologies', 'SensorEdge_Solutions', 'DataFusion_Sensors', 'Echelon_Sensing_Solutions', 'ProSync_Sensors', 'VitalSense_Dynamics', 'ApexSensors_Technologies')),
                    # "location": fake.location()
                },
                "timestamp": timestamp,
                "currentConditions": {
                    "windDirection": float(Decimal(fake.random_int(min=0, max=3600)) / 10),
                    "tempF": float(Decimal(fake.random_int(min=500, max=900)) / 10),
                    "windSpeed": float(Decimal(fake.random_int(min=0, max=100)) / 10),
                    "cloudCover": None if fake.random_element(elements=(None, 1)) is None else float(Decimal(fake.random_int(min=0, max=1000)) / 10),
                    "precip": float(Decimal(fake.random_int(min=0, max=100)) / 10),
                    "humidity": float(Decimal(fake.random_int(min=0, max=1000)) / 10)
                }
            }
            # Ingest data into MongoDB
            collection.insert_one(data_point)
            current_date += timedelta(seconds=granularity)

# Get user input with default values
duration_days_input = input("Enter the number of days (default is 1): ")
granularity_unit_input = input("Enter the granularity unit ('second', 'minute', 'hour', default is 'hour'): ")

# Set default values if the user didn't provide any
duration_days = int(duration_days_input) if duration_days_input else 1
granularity_unit = granularity_unit_input.lower() if granularity_unit_input else 'hour'
granularity = 1 if granularity_unit == 'second' else 60 if granularity_unit == 'minute' else 3600

# Generate and ingest random data into MongoDB
generate_and_ingest_data(duration_days, granularity, granularity_unit)

print("Data generation and ingestion completed.")

## todo : will implement multi threads to ingest the data 