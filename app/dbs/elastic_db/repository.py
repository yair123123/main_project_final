from typing import List, Dict

from app.dbs.elastic_db.database import create_index
from app.settings.config_dbs import elastic_client


def insert_many_descriptions(description: List[Dict[str, str]]) -> None:
    create_index("events")
    try:
        for x in description:
            elastic_client.index(index="events", body=x)
    except Exception as e:
        print(e)



def search(text):
    query = {
        "size":1000,
        "query": {

            "match": {
                "summary": text
            }
        }
    }

    response = elastic_client.search(index="events", body=query)
    return response
