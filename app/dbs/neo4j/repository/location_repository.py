from typing import List, Set

from returns.maybe import Maybe

from app.settings.config_dbs import driver
def insert_many_location(locations:Set[str]):
    with driver.session() as session:
        try:
            query="""
            UNWIND $locations AS location
            MERGE (r:Region {name:location.region})
            MERGE (u:Country {name: location.country})
            MERGE (c:City {name:location.city})
            MERGE (u) - [:IN] -> (r) - [:IN] -> (c)
            """
            parm = {"locations":locations}
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