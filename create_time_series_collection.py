import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://XXX")
db = client["tsDb"]  # Replace 'your_database_name' with your actual database name

# Define the options for the time-series collection
timeseries_options = {
    'timeseries': {
        'timeField': 'timestamp',
        'metaField': 'metadata',
        'granularity': 'seconds'
    }
}

# Create the time-series collection
collection_name = 'tsw_info_sec_900_1200'
db.create_collection(collection_name, **timeseries_options)

print(f"Time-series collection '{collection_name}' created successfully.")
