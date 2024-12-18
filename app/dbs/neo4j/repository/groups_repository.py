import itertools
from typing import List, Set

from returns.maybe import Maybe

from app.settings.config_dbs import driver

def insert_many_groups(groups:Set[List[str]]):
    groups = {item for group in groups for item in group if item}
    with driver.session() as session:
        try:
            query="""
            UNWIND $groups AS group
            CREATE (u:Group {name: group})
            """
            parm = {"groups":groups}
            session.run(query,parm)
        except Exception as e:
            print(e)

def insert_group(name:str):
    with driver.session() as session:
        query = """
        merge (a:Group {name :$name})
        return a
        """
        params = {"name":name}
        res = Maybe.from_optional(session.run(query,params).single())
        return res