from typing import List, Set

from returns.maybe import Maybe

from app.settings.config_dbs import driver

def insert_many_target(targets:Set[str]):
    with driver.session() as session:
        try:
            query="""
            UNWIND $targets AS target
            CREATE (u:TargetType {type: target})
            """
            parm = {"targets":targets}
            session.run(query,parm)
        except Exception as e:
            print(e)
def insert_target_type(type:str):
    with driver.session() as session:
        query = """
        merge (a:TargetType {type: $type})
        return a
        """
        params = {"type":type}
        res = Maybe.from_optional(session.run(query,params).single())
        return res