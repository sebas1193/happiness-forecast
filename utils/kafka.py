from json import dumps, loads
import joblib
from kafka import KafkaProducer, KafkaConsumer
import pandas as pd
from utils.db_postgres import insert_data
import logging
import six

joblib_file = "/app/models/xgboost_model.joblib"
model = joblib.load(joblib_file)

def kafka_producer(row):
    producer = KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['kafka:9092'],
    )

    message = row.to_dict()
    producer.send('kafka-happiness', value=message)
    logging.info("Message sent")

def kafka_consumer():
    consumer = KafkaConsumer(
        'kafka-happiness',
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['kafka:9092']
    )

    for message in consumer:
        df = pd.json_normalize(data=message.value)
        df['happiness_prediction'] = model.predict(df[['GDP_per_capita',
                                                        'life_expectancy',
                                                        'freedom',
                                                        'perceptions_corruption',
                                                        'generosity',
                                                        'continent_numeric']])
        insert_data(df.iloc[0])
        logging.info("Data inserted into PostgreSQL and Data:\n", df)


