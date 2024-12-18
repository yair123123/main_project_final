from typing import List, Dict

from pymongo.errors import PyMongoError
from returns.result import Success, Failure

from app.settings.config_dbs import events_collection


def insert_many_events(events:List[Dict[str,str]]):
    try:
        events = events_collection.insert_many(events).inserted_ids
        return Success(events)
    except PyMongoError as e:
        return Failure(str(e))