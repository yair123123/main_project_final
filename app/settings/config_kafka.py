import json
import os

from kafka import KafkaConsumer


def consume_and_save(topic_env_var, save_function):
    consumer = KafkaConsumer(
        os.environ[topic_env_var],
        bootstrap_servers=os.environ['BOOTSTRAP_SERVER'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest'
    )
    print(f'Listening to topic: {os.environ[topic_env_var]}')
    for message in consumer:
        save_function(message.value)
        print(f'Received: {message.key} : {message.value}')
