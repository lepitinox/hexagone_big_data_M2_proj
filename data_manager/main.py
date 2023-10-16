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
    producer.produce(TOPIC, key=str(key), value=value)
    producer.flush()


if __name__ == '__main__':
    client = dataikuapi.APINodeClient("https://api-56ce4d5f-779f448b-dku.eu-west-3.app.dataiku.io/", "US_Census")

    while True:
        start = time.time()
        result = client.run_function("generate_census_records")
        new_census_record = result.get("response")
        end = time.time()
        print("Time to call api: ", end - start)
        print(new_census_record)
        publish("rep", json.dumps(new_census_record).encode("utf-8"))
        time.sleep(10)
