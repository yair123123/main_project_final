from typing import List, Set

from returns.maybe import Maybe

from app.settings.config_dbs import driver
def insert_many_location(locations:Set[str]):
    if locations is None:
        return
    with driver.session() as session:
        try:
            query="""
            UNWIND $locations AS location
            MERGE (r:Region {name: location.region})
            MERGE (u:Country {name: location.country})
            MERGE (c:City {name: location.city})
            
            MERGE (c)-[rel_city_country:IN]->(u)
            ON CREATE SET rel_city_country.created_at = timestamp()
            
            MERGE (u)-[rel_country_region:IN]->(r)
            ON CREATE SET rel_country_region.created_at = timestamp()

            """
            parm = {"locations":list(locations)}
            session.run(query,parm)
        except Exception as e:
            print(e)

def insert_country(country:str):
    with driver.session() as session:
        query = """
        merge (c:Country {name:name})
        return c
        """
        params = {"name":country}
        res = Maybe.from_optional(session.run(query,params).single())
        return res