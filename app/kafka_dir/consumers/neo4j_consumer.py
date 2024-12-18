from threading import Thread

from app.settings.config_kafka import consume_and_save


def run_all_consumers_neo4j_parallel():
    consumers = [
        ('TOPIC_NEO4J_REGION', insert_many_region),
        ('TOPIC_NEO4J_COUNTRY', insert_many_students),
        ('TOPIC_NEO4J_CITY', insert_many_students),
        ('TOPIC_NEO4J_GROUPS', insert_many_classes),
        ('TOPIC_NEO4J_ATTACK_TYPE', insert_many_relationships),
        ('TOPIC_NEO4J_TARGET_TYPE', insert_many_relationships),
        ('TOPIC_NEO4J_EVENT', insert_many_teachers),
    ]

    threads = [
        Thread(target=consume_and_save, args=(topic_env, save_func))
        for topic_env, save_func in consumers
    ]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

if __name__ == '__main__':
    run_all_consumers_neo4j_parallel()
