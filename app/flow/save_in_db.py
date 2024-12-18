import itertools
from typing import List, Dict

from toolz import pluck, get_in

from app.dbs.neo4j.repository.attack_type_repository import insert_many_attack_types
from app.dbs.neo4j.repository.location_repository import insert_country, insert_many_countries, \
    insert_many_regions_and_countries
from app.dbs.neo4j.repository.event_repository import insert_many_events
from app.dbs.neo4j.repository.groups_repository import insert_group, insert_many_groups
from app.dbs.neo4j.repository.region_repository import insert_many_regions
from app.dbs.neo4j.repository.target_type_repository import insert_many_target


def convert_event_to_save(event: Dict[str, Dict[str, str]]):
    return {"eventid": event.get("event_id"),
            **event.get("data"),
            "country": get_in(["location", "country"], event),
            "attack_type": get_in(["attack", "attack_type"], event),
            "target_type": get_in([["target", "target_type"]], event),
            "groups":event.get("groups") }


def save_in_neo4j(events: List[Dict[str, Dict[str, str]]]):
    extractors = {
        "location": (["location"], insert_many_regions_and_countries),
        "groups": ("groups", insert_many_groups),
        "attack_type": (["attack", "attack_type"], insert_many_attack_types),
        "target_type": (["target", "target_type"], insert_many_target),
    }

    for key, (pluck_keys, insert_func) in extractors.items():
        extracted = set(pluck(pluck_keys, events))
        insert_func(extracted)

    slim_event = [convert_event_to_save(d) for d in events]
    insert_many_events(slim_event)