from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

i = 0
while True:
    message = f"Message {i}"
    producer.send('test-topic', message.encode('utf-8'))
    print(f"Sent: {message}")
    i += 1
    time.sleep(1)

# No need to call flush here unless you exit
