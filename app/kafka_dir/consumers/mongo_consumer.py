from dotenv import load_dotenv

from app.dbs.mongodb.repository import insert_many_events
from app.settings.config_kafka import consume_and_save
load_dotenv(verbose=True)

def consume_and_save_in_mongodb():
    consume_and_save('TOPIC_MONGO', insert_many_events)

if __name__ == '__main__':
    consume_and_save_in_mongodb()