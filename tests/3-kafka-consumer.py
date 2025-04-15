from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'automotive-logs',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='test-group',
)

print("Listening for messages on 'automotive-logs'...")

for message in consumer:
    print(f"Received: {message.value.decode('utf-8')}")
