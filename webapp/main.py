import sys
from confluent_kafka import Consumer, KafkaError, KafkaException
import json
from dotenv import load_dotenv
import os
import dataikuapi
from pathlib import Path
import streamlit as st
import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts

client = dataikuapi.APINodeClient("https://api-56ce4d5f-779f448b-dku.eu-west-3.app.dataiku.io/", "AdriPI")
load_dotenv()

path = Path(os.getenv('KAFKA_CONFIG', 'kafka_config.json'))
data = path.read_text()

TOPIC = os.getenv('KAFKA_TOPIC_NAME', 'new_transactions')
config = json.loads(data)

consumer = Consumer(config)

running = True

topics = [TOPIC]

typess = {'age': 'int', 'class of worker': 'str', 'industry code': 'int', 'occupation code': 'int', 'education': 'str', 'wage per hour': 'int', 'enrolled in edu inst last wk': 'str', 'marital status': 'str', 'major industry code': 'str', 'major occupation code': 'str', 'race': 'str', 'hispanic Origin': 'str', 'sex': 'str', 'member of a labor union': 'str', 'reason for unemployment': 'str', 'full or part time employment stat': 'str', 'capital gains': 'int', 'capital losses': 'int', 'divdends from stocks': 'int', 'tax filer status': 'str', 'region of previous residence': 'str', 'state of previous residence': 'str', 'detailed household and family stat': 'str', 'detailed household summary in household': 'str', 'instance weight': 'float', 'migration code-change in msa': 'str', 'migration code-change in reg': 'str', 'migration code-move within reg': 'str', 'live in this house 1 year ago': 'str', 'migration prev res in sunbelt': 'str', 'num persons worked for employer': 'int', 'family members under 18': 'str', 'country of birth father': 'str', 'country of birth mother': 'str', 'country of birth self': 'str', 'citizenship': 'str', 'own business or self employed': 'int', "fill inc questionnaire for veteran's admin": 'str', 'veterans benefits': 'int', 'weeks worked in year': 'int', 'year': 'int', 'income level': 'str'}


def nulachier(values):
    req: dict = json.loads(values.decode('utf8'))
    expected = req.pop("income level")
    time_stamp = req.pop("timestamp")
    print(time_stamp)
    print(req)
    temp = {i: eval(typess[i])(j) for i, j in req.items()}
    prediction = client.predict_record("model_classifier", temp)
    ret = prediction["result"]
    print(f"expected: {expected}, got: {ret['prediction']}")
    return ret




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
            res = nulachier(msg.value())
            st.write(res)

finally:
    # Close down consumer to commit final offsets.
    consumer.close()
