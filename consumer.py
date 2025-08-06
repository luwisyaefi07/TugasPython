from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_SERVER = ["5.189.154.248:9092"]
IOT_TOPIC = "luwi_iot_data"
ALERT_TOPIC = "luwi_alerts"

consumer = KafkaConsumer(
    IOT_TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    group_id="iot_group",  
    auto_offset_reset="earliest",  
    enable_auto_commit=True
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Consumer Aktif: Menunggu data IOT...")

for message in consumer:
    data = message.value
    print(f"[Diterima] {data}")
    if data["temperature"] > 95:
        print("ALERT: High Temperature!")
        producer.send(ALERT_TOPIC, value=data)
        producer.flush()