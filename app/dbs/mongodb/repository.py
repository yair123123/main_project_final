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


def most_deadly(top_n=None):
    pipeline = [
        {
            "$match": {
                "attack.attack_type": {"$ne": None}
            }
        },
        {
            "$project": {
                "_id": 0,
                "attacktype": "$attack.attack_type",
                "total_casualties_and_wounded": {
                    "$add": [
                        {"$multiply": ["$result.num_spread", 1]},
                        {"$multiply": ["$result.num_killed", 2]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$attacktype",
                "total_casualties_and_wounded": {"$sum": "$total_casualties_and_wounded"}
            }
        },
        {
            "$sort": {"total_casualties_and_wounded": -1}
        }
    ]

    if top_n:
        pipeline.append({
            "$limit": top_n
        })

    result = events_collection.aggregate(pipeline)
    return list(result)


def average_casualties_by_area(top_n=None):
    pipeline = [
        {
            "$match": {
                "attack.attack_type": {"$ne": None},
                "location.latitude": {"$ne": None},
                "location.longitude": {"$ne": None}
            }
        },
        {
            "$project": {
                "_id": 0,
                "latitude": "$location.latitude",
                "longitude": "$location.longitude",
                "total_casualties_and_wounded": {
                    "$add": [
                        {"$multiply": ["$result.num_spread", 1]},
                        {"$multiply": ["$result.num_killed", 2]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "region":"$location.region"
                },
                "average_casualties": {"$avg": "$total_casualties_and_wounded"}
            }
        },
        {
            "$sort": {"average_casualties": -1}
        }
    ]

    if top_n:
        pipeline.append({
            "$limit": top_n
        })

    result = events_collection.aggregate(pipeline)
    return list(result)
