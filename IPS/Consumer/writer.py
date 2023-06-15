from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('scraped_data',
                         bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                         auto_offset_reset='earliest',
                         enable_auto_commit=True)

