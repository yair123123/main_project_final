from app.dbs.elastic_db.repository import search
from app.dbs.mongodb.repository import get_events_by_eventid


def get_news_from_elastic(text):
    res = [x['_source'] for x in search(text)['hits']['hits']]
    res = [get_events_by_eventid(r['eventid']) for r in res]
    return res


def get_all_from_elastic(text):
    res = [x['_source'] for x in search(text)['hits']['hits']]
    res = [get_events_by_eventid(r['eventid']) for r in res]
    return res


def get_history_from_elastic(text):
    res = [x['_source'] for x in search(text)['hits']['hits']]
    res = [get_events_by_eventid(r['eventid']) for r in res]
    return res


def get_all_from_elastic_by_date(text, start_date, end_date):
    res = [x['_source'] for x in search(text)['hits']['hits']]
    res = [get_events_by_eventid(r['eventid']) for r in res]
    return res
