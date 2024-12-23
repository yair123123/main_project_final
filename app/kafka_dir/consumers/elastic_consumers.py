from dotenv import load_dotenv

from app.dbs.elastic_db.repository import insert_many_descriptions
from app.settings.config_kafka import consume_and_save

load_dotenv(verbose=True)


def consume_and_save_in_elastic():
    consume_and_save('TOPIC_CONSUME_ELASTIC', insert_many_descriptions)


if __name__ == '__main__':
    consume_and_save_in_elastic()
