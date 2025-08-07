import json
import psycopg2
import os
from kafka import KafkaConsumer
from redis import Redis
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Kafka Configuration
KAFKA_SERVER = os.getenv("KAFKA_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

# Postgres Configuration
conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        dbname=os.getenv("DB"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        port=int(os.getenv("PORT"))
    )

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

cursor = conn.cursor()
redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='website_access_l'
)

def block_ip(ip):
    now = datetime.utcnow()
    cursor.execute(
        "INSERT INTO blocked_ip_address (ip_address, blocked_at) VALUES (%s, %s)",
        (ip, now)
    )
    conn.commit()
    print(f"IP {ip} | BLOCKED at {now}")

print("Consumer Aktif: Menunggu data web access...")

for message in consumer:
    data = message.value
    ip = data["ip_address"]

    key = f"access:{ip}"
    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, 60)  

    print(f"Access from {ip} ➝ count: {count}")

    if count > 10:
        if not redis_client.get(f"blocked:{ip}"):
            block_ip(ip)
            redis_client.setex(f"blocked:{ip}", 3600, 1)  