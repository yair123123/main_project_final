from app.dbs.mongodb.repository import get_point_by_region


def test_mongo_convert_point():
    region = 'Australasia & Oceania'
    points = get_point_by_region(region)
    print(points)
    assert points