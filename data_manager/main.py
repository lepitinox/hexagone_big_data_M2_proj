import time

from confluent_kafka import Producer
import json
from dotenv import load_dotenv
import os
import dataikuapi
load_dotenv()

TOPIC = os.getenv('KAFKA_TOPIC_NAME', 'new_transactions')
config = json.loads(os.getenv('KAFKA_CONFIG', 'config.json'))

producer = Producer(config)


def publish(key, value):
    producer.produce(TOPIC, key=str(key), value=str(value))
    producer.flush()


if __name__ == '__main__':
    client = dataikuapi.APINodeClient("https://api-56ce4d5f-779f448b-dku.eu-west-3.app.dataiku.io/", "US_Census")

    while True:
        result = client.run_function("generate_census_records")
        new_census_record = str(result.get("response"))
        publish("rep", new_census_record)
        time.sleep(10)
