#!/bin/bash

# רשימת ה-Topics
topics=(
    "elastic"
    "mongo"
    "neo_attack"
    "neo_event"
    "neo_group"
    "neo_location"
    "neo_target"
    "streaming-__assignor-__leader"
    "topic_process1"
    "topic_process2"
)

# שרת Kafka
bootstrap_server="broker0:29092"

# לולאה ליצירת פקודות מחיקה
for topic in "${topics[@]}"; do
    echo "docker container exec -it cli-tools kafka-topics --bootstrap-server $bootstrap_server --delete --topic $topic"
done
