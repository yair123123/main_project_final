from elasticsearch import Elasticsearch
from neo4j import GraphDatabase
from pymongo import MongoClient




# mongodb
mongo_client = MongoClient("mongodb://172.29.168.75:27017/")
mongo_db = mongo_client["terrorism"]
events_collection = mongo_db["events"]


# neo4g
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "pwd1234567890"
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

# elastic
elastic_client = Elasticsearch(['http://localhost:9200'])


