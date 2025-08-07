import json
import time
import os
from kafka import KafkaProducer
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Kafka Configuration
KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# IP Adress
IP_ADRESS = os.getenv("IP_ADRESS")

producer = KafkaProducer(
    bootstrap_servers = KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def user_behaviour():
    user_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "url": "https://redis.io/docs/latest/develop/clients/redis-py/connect/",
        "ip_address": IP_ADRESS
    }

    producer.send(KAFKA_TOPIC, value=user_data)
    print(f"Terkirim: {user_data}")

if __name__ == "__main__":
    print("Proses dimulai: Mengirim data...")
    while True:
        user_behaviour()
        time.sleep(5)

