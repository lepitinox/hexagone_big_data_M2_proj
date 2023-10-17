import sys
from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from dotenv import load_dotenv
import os
import dataikuapi
from pathlib import Path
import streamlit as st
import pandas as pd

client = dataikuapi.APINodeClient("https://api-56ce4d5f-779f448b-dku.eu-west-3.app.dataiku.io/", "AdriPI")
load_dotenv()

path = Path(os.getenv('KAFKA_CONFIG', '../backend/kafka_config.json'))
data = path.read_text()

TOPIC = os.getenv('KAFKA_TOPIC_NAME', 'new_transactions')
config = json.loads(data)

consumer = Consumer(config)

running = True

topics = [TOPIC]

typess = {'age': 'int', 'class of worker': 'str', 'industry code': 'int', 'occupation code': 'int', 'education': 'str',
          'wage per hour': 'int', 'enrolled in edu inst last wk': 'str', 'marital status': 'str',
          'major industry code': 'str', 'major occupation code': 'str', 'race': 'str', 'hispanic Origin': 'str',
          'sex': 'str', 'member of a labor union': 'str', 'reason for unemployment': 'str',
          'full or part time employment stat': 'str', 'capital gains': 'int', 'capital losses': 'int',
          'divdends from stocks': 'int', 'tax filer status': 'str', 'region of previous residence': 'str',
          'state of previous residence': 'str', 'detailed household and family stat': 'str',
          'detailed household summary in household': 'str', 'instance weight': 'float',
          'migration code-change in msa': 'str', 'migration code-change in reg': 'str',
          'migration code-move within reg': 'str', 'live in this house 1 year ago': 'str',
          'migration prev res in sunbelt': 'str', 'num persons worked for employer': 'int',
          'family members under 18': 'str', 'country of birth father': 'str', 'country of birth mother': 'str',
          'country of birth self': 'str', 'citizenship': 'str', 'own business or self employed': 'int',
          "fill inc questionnaire for veteran's admin": 'str', 'veterans benefits': 'int',
          'weeks worked in year': 'int', 'year': 'int', 'income level': 'str'}


def is_good(s):
    return ['background-color: green'] * len(s) if s.good_prediction else ['background-color: red'] * len(s)


def nulachier(values, idx):
    req: dict = json.loads(values.decode('utf8'))
    df = pd.DataFrame(req, index=[idx])
    expected = req.pop("income level")
    time_stamp = req.pop("timestamp")
    print(time_stamp)
    print(req)
    temp = {i: eval(typess[i])(j) for i, j in req.items()}
    prediction = client.predict_record("model_classifier", temp)
    df["prediction"] = prediction["result"]["prediction"]
    df["good_prediction"] = df["prediction"] == expected
    ret = prediction["result"]
    print(f"expected: {expected}, got: {ret['prediction']}")
    return df


dff = None
ind = 0
pct = st.empty()
test = st.empty()

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

            print("doing int")

            res = nulachier(msg.value(), ind)
            ind += 1
            if dff is None:
                dff = res
            else:
                dff = pd.concat([dff, res])
            dff.to_csv("/data/dataset.csv")

finally:
    # Close down consumer to commit final offsets.
    consumer.close()
