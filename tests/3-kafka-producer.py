from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_log():
    return {
        "vehicle_id": f"CAR{random.randint(1, 10)}",
        "timestamp": time.time(),
        "speed": round(random.uniform(20, 150), 2),
        "engine_temp": round(random.uniform(70, 120), 2),
        "location": {
            "lat": round(random.uniform(-90, 90), 6),
            "lon": round(random.uniform(-180, 180), 6)
        }
    }

while True:
    log = generate_log()
    print(f"Sending: {log}")
    producer.send('automotive-logs', log)
    time.sleep(1)
