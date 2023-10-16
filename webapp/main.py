import sys
from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from dotenv import load_dotenv
import os

load_dotenv()

TOPIC = os.getenv('KAFKA_TOPIC_NAME', 'new_transactions')
config = json.loads(os.getenv('KAFKA_CONFIG', 'config.json'))

consumer = Consumer(config)

running = True

topics = [TOPIC]

try:
    consumer.subscribe(topics)

    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            print(str(msg.key()) + str(msg.value()))

finally:
    # Close down consumer to commit final offsets.
    consumer.close()
