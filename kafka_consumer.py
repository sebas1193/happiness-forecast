from utils.kafka import kafka_consumer
from utils.db_postgres import create_table
import six

if __name__ == "__main__":
    create_table()
    kafka_consumer()