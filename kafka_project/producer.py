import json
import time
import random
import os
from kafka import KafkaProducer
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_SERVER")
IOT_TOPIC = os.getenv("IOT_TOPIC")

produser = KafkaProducer(
    bootstrap_servers = KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def create_data():
    for id in range(1,6):
        device_data = {
            "device_id" : f"device_{id}",
            "temperature" : round(random.uniform(1,100)),
            "humidity" : round(random.uniform(20,30),2),
            "timestamp" : datetime.utcnow().isoformat(),
            "location" : random.choice(["Cirebon", "Indramayu", "Majalengka", "Kuningan", "Sumedang"])
        }
        produser.send(IOT_TOPIC, value=device_data)
        print(f"Berhasil terkirim")
    produser.flush()

scheduler = BlockingScheduler()
scheduler.add_job(create_data, 'cron', minute='*')
print("Schedule Aktif: mengirimkan data setiap 1 menit...")
scheduler.start()
