from typing import List, Dict

from app.dbs.elastic_db.database import create_index
from app.settings.config_dbs import elastic_client


def insert_many_descriptions(description:List[Dict[str,str]]) -> None:
    create_index("events")
    try:
        for x in description:
            elastic_client.index(index="events", body=x)
    except Exception as e:
        print(e)
a = {
  "review_id": "12345abcde",
  "content": "This app is amazing! The user interface is intuitive and responsive.",
  "score": 4.5,
  "date_time": "15-12-2024 14:30",
  "thumbs_up_count": 125,
  "review_created_version": "1.3.0",
  "app_version": "1.5.2",
  "student_id": 987654
}
