from typing import List, Set

from returns.maybe import Maybe

from app.settings.config_dbs import driver
def insert_many_regions(regions:Set[str]):
    regions = set(regions)
    with driver.session() as session:
        try:
            query="""
            UNWIND $regions AS region
            MERGE (u:Regions {name: region})
            """
            parm = {"regions":list(regions)}
            session.run(query,parm)
        except Exception as e:
            print(e)

def insert_region(name:str):
    with driver.session() as session:
        query = """
        merge (a:Region {name: $name})
        return a
        """
        params = {"name":name}
        res = Maybe.from_optional(session.run(query,params).single())
        return res