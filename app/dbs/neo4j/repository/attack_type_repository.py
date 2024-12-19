from typing import List

from returns.maybe import Maybe

from app.settings.config_dbs import driver


def insert_many_attack_types(attack_types: List[str]):
    attack_types = set(attack_types)
    with driver.session() as session:
        try:
            query = """
            UNWIND $attack_types AS attack_type
            MERGE (u:AttackedType {type: attack_type})
            """
            parm = {"attack_types": list(attack_types)}
            session.run(query, parm)
        except Exception as e:
            print(e)


def insert_attack_type(attack_type: str):
    with driver.session() as session:
        query = """
        merge (a:AttackedType {type:$type})
        return a
        """
        params = {"type": attack_type}
        res = Maybe.from_optional(session.run(query, params).single())
        return res
