from typing import List, Dict

from pymongo.errors import PyMongoError
from returns.result import Success, Failure

from app.settings.config_dbs import events_collection

def get_point_by_country(country:str):
    pipeline = [
        {
            "$match": {"location.country": country,"location.longitude": {"$nin":[None,float('nan')]},"location.latitude": {"$nin":[None,float('nan')]}},

        },
        {
            "$project": {
                "_id": 0,
                "location.latitude": 1,
                "location.longitude": 1,
            }
        },
        {
            "$limit": 1,
        }
    ]
    result = events_collection.aggregate(pipeline).next()
    return result.get("location",{})
def get_point_by_region(region:str):
    pipeline = [
        {
            "$match": {"location.region": region,"location.longitude": {"$ne":None},"location.latitude": {"$ne":None}},
        },
        {
            "$project": {
                "_id": 0,
                "location.latitude": 1,
                "location.longitude": 1,
            }
        },
        {
            "$limit": 1,
        }

    ]
    result = events_collection.aggregate(pipeline).next()
    return result.get("location",{})

def insert_many_events(events: List[Dict[str, str]]):
    try:
        events = events_collection.insert_many(events).inserted_ids
        return Success(events)
    except PyMongoError as e:
        return Failure(str(e))


def most_deadly(top_5=None):
    pipeline = [
        {
            "$match": {
                "attack.attack_type": {"$ne": None},
                "result.num_spread": {"$nin":[float('nan')]},
                "result.num_killed":{"$nin":[float('nan')]}
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

    if top_5:
        pipeline.append({
            "$limit": 5
        })

    result = events_collection.aggregate(pipeline)
    return list(result)


def average_casualties_by_area(top_5=None):
    pipeline = [
        {"$addFields": {
            "result.num_spread": {
                "$cond": [
                    {"$eq": ["$result.num_spread", float('nan')]}, 0, "$result.num_spread"
                ]

            },
            "result.num_killed": {
                "$cond": [
                    {"$eq": ["$result.num_killed", float('nan')]}, 0, "$result.num_killed"
                ]
            }
        }},
        {"$match": {
            "location.latitude": {"$nin": [None,float('nan')]},
            "location.longitude": {"$nin": [None,float('nan')]},
            "location.region": {"$nin": [None, 'nan']},
            "result.num_spread": {"$ne": None},
            "result.num_killed": {"$ne": None}
        }},
        {"$project": {
            "_id": 0,
            "location.region": 1,
            "location.latitude": 1,
            "location.longitude": 1,
            "total_casualties_and_wounded": {
                "$add": [
                    {"$multiply": [{"$ifNull": ["$result.num_spread", 0]}, 1]},
                    {"$multiply": [{"$ifNull": ["$result.num_killed", 0]}, 2]}
                ]
            }
        }},
        {
            "$group": {
                "_id": {
                    "region": "$location.region"
                },
                "latitude": {"$first": "$location.latitude"},
                "longitude": {"$first": "$location.longitude"},
                "average_casualties": {"$avg": "$total_casualties_and_wounded"}
            }
        },
        {
            "$sort": {"average_casualties": -1}
        }
    ]

    if top_5:
        pipeline.append({
            "$limit": 5
        })

    result = events_collection.aggregate(pipeline)
    return list(result)


def top_5_most_num_spread():
    pipeline = [
        {"$addFields": {
            "result.num_spread": {
                "$cond": [
                    {"$eq": ["$result.num_spread", float('nan')]}, 0, "$result.num_spread"
                ]
            },
            "result.num_killed": {
                "$cond": [
                    {"$eq": ["$result.num_killed", float('nan')]}, 0, "$result.num_killed"
                ]
            }
        }},
        {"$unwind": "$groups"},
        {"$match": {
            "groups": {"$ne": None},
            "result.num_spread": {"$ne": None},
            "result.num_killed": {"$ne": None}
        }},
        {"$project": {
            "_id": 0,
            "groups": 1,
            "total_casualties_and_wounded": {
                "$add": [
                    {"$multiply": [{"$ifNull": ["$result.num_spread", 0]}, 1]},
                    {"$multiply": [{"$ifNull": ["$result.num_killed", 0]}, 2]}
                ]
            }
        }},
        {
            "$group": {
                "_id": {
                    "group": "$groups"
                },
                "average_casualties": {"$sum": "$total_casualties_and_wounded"}
            }
        },
        {
            "$sort": {"average_casualties": -1}
        },
        {
            "$limit": 5
        }
    ]
    result = events_collection.aggregate(pipeline)
    return list(result)


def most_group_active_by_region():
    pipeline = [
        {"$addFields": {
            "result.num_spread": {
                "$ifNull": [{"$cond": [{"$in": ["$result.num_spread", [None, "nan"]]}, 0, "$result.num_spread"]}, 0]
            },
            "result.num_killed": {
                "$ifNull": [{"$cond": [{"$in": ["$result.num_killed", [None, "nan"]]}, 0, "$result.num_killed"]}, 0]
            }
        }},
        {"$unwind": "$groups"},
        {"$match": {
            "groups": {"$ne": None},
            "location.region": {"$nin": [None, "nan"]},
            "location.latitude": {"$nin": [None, "nan",float('nan')]},
            "location.longitude": {"$nin": [None, "nan",float('nan')]},
            "result.num_spread": {"$gte": 0},
            "result.num_killed": {"$gte": 0}
        }},
        {"$project": {
            "_id": 0,
            "location.region": 1,
            "groups": 1,
            "total_casualties_and_wounded": {
                "$add": [
                    {"$multiply": ["$result.num_spread", 1]},
                    {"$multiply": ["$result.num_killed", 2]}
                ]
            },
            "location.latitude": 1,
            "location.longitude": 1
        }},
        {"$group": {
            "_id": {
                "region": "$location.region",
                "group": "$groups"
            },
            "total_casualties": {"$sum": "$total_casualties_and_wounded"},
            "latitude": {"$first": "$location.latitude"},
            "longitude": {"$first": "$location.longitude"}
        }},
        {"$group": {
            "_id": "$_id.region",
            "top_groups": {
                "$push": {
                    "group": "$_id.group",
                    "total_casualties": "$total_casualties"
                }
            },
            "latitude": {"$first": "$latitude"},
            "longitude": {"$first": "$longitude"}
        }},
        {"$project": {
            "top_groups": {
                "$slice": [{"$sortArray": {"input": "$top_groups", "sortBy": {"total_casualties": -1}}}, 5]
            },
            "latitude": 1,
            "longitude": 1
        }},
        {"$sort": {"_id": 1}}
    ]

    result = events_collection.aggregate(pipeline)
    return list(result)


def history_events_by_year(year):
    pipeline = [
        {
            "$match": {
                "location.latitude": {"$nin": [None, "nan", "NaN", float('nan')]},
                "location.longitude": {"$nin": [None, "nan", "NaN", float('nan')]},
                "date.year": {"$gte": year}
            }

        },
        {
            "$project": {
                "_id": 0,
                "location.longitude": 1,
                "location.latitude": 1
            }
        }
    ]

    result = events_collection.aggregate(pipeline)
    return list(result)


def get_events_by_eventid(event_id):
    pipeline = [
        {
            "$match": {
                'eventid': event_id,
                "location.latitude": {"$nin": [None, "nan", float('nan')]},
                "location.longitude": {"$nin": [None, "nan", float('nan')]}
            }


        },
        {
            "$project": {
                "_id": 0
            }
        }
    ]

    result = events_collection.aggregate(pipeline)
    try:
        return next(result)
    except StopIteration:
        return None
