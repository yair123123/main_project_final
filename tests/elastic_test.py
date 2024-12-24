from app.dbs.elastic_db.repository import search
from app.flow.elastic_service import get_news_from_elastic


def test_search():
    res = search("hamas")
    print(res)
def test_search1():
    res = get_news_from_elastic("a")
    print(res)