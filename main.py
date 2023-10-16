import time

from confluent_kafka import Producer
import json
from dotenv import load_dotenv
import os
import dataikuapi
from pathlib import Path

load_dotenv()

path = Path(os.getenv('KAFKA_CONFIG', 'kafka_config.json'))
data = path.read_text()

TOPIC = os.getenv('KAFKA_TOPIC_NAME', 'new_transactions')
config = json.loads(data)

producer = Producer(config)


def publish(key, value):
    producer.produce(TOPIC, key=str(key), value=str(value))
    producer.flush()


if __name__ == '__main__':
    client = dataikuapi.APINodeClient("https://api-56ce4d5f-779f448b-dku.eu-west-3.app.dataiku.io/", "US_Census")

    result = client.run_function("generate_census_records")
    res = result.get("response")
    print(type(res))
    print(res)
    publish("rep", res)
