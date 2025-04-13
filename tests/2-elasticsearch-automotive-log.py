from elasticsearch import Elasticsearch
import random
import time
from faker import Faker
from datetime import datetime
import pytz

# Initialize Elasticsearch and Faker
es = Elasticsearch("http://localhost:9200")
fake = Faker()

# Function to generate automotive log data
def generate_automotive_log():
    return {
        "vehicle_id": fake.uuid4(),  # Unique Vehicle ID
        "timestamp": datetime.now(pytz.utc).replace(microsecond=0).isoformat(),
        "speed": random.randint(0, 120),  # Vehicle speed (0-120 km/h)
        "rpm": random.randint(800, 4000),  # Engine RPM (800 to 4000)
        "fuel_level": random.randint(0, 100),  # Fuel level (percentage)
        "engine_temp": random.randint(60, 120),  # Engine temperature in Celsius
        "battery_voltage": round(random.uniform(11.5, 14.5), 2),  # Battery voltage (11.5 to 14.5V)
        "gps_coordinates": {
            "latitude": round(random.uniform(-90, 90), 6),  # Latitude between -90 and 90
            "longitude": round(random.uniform(-180, 180), 6),  # Longitude between -180 and 180
        },
        "odometer": random.randint(5000, 200000),  # Odometer reading (5,000 to 200,000 km)
        "error_codes": [f"DT{random.randint(1000, 9999)}" for _ in range(random.randint(0, 3))]  # Random error codes
    }

# Example of generating a single log
log = generate_automotive_log()

# If you want to continuously insert data into Elasticsearch
# (assuming es is your Elasticsearch client)

# for example, sending data to Elasticsearch every 2 seconds
while True:
    log = generate_automotive_log()
    es.index(index="automotive-logs", document=log)
    print(f"Inserted document: {log}")
    time.sleep(0.1)  # Wait 2 seconds before sending the next log
