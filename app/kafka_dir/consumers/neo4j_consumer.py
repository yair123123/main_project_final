from threading import Thread

from app.dbs.neo4j.repository.attack_type_repository import insert_many_attack_types
from app.dbs.neo4j.repository.event_repository import insert_many_events
from app.dbs.neo4j.repository.groups_repository import insert_many_groups
from app.dbs.neo4j.repository.location_repository import  insert_many_location
from app.dbs.neo4j.repository.target_type_repository import insert_many_target
from app.settings.config_kafka import consume_and_save


def run_all_consumers_neo4j_parallel():
    consumers = [
        ('TOPIC_CONSUME_NEO4J_LOCATION', insert_many_location),
        ('TOPIC_CONSUME_NEO4J_GROUPS', insert_many_groups),
        ('TOPIC_CONSUME_NEO4J_ATTACK', insert_many_attack_types),
        ('TOPIC_CONSUME_NEO4J_TARGET', insert_many_target),
        ('TOPIC_CONSUME_NEO4J_EVENT', insert_many_events),
    ]

    threads = [
        Thread(target=consume_and_save, args=(topic_env, save_func))
        for topic_env, save_func in consumers
    ]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


if __name__ == '__main__':
    run_all_consumers_neo4j_parallel()
