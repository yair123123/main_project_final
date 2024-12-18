from typing import List, Dict

from returns.maybe import Maybe

from app.settings.config_dbs import driver

def insert_many_events(events:List[Dict[str,Dict[str,str]]]):

    with driver.session() as session:
            try:
                query="""
                UNWIND $events AS event
                MATCH (c:Country {name:event.country}),
                    (g:Group{name:event.groups}),
                    (at:AttackType{type:event.attack_type}),
                    (ta:TargetType{type:event.target_type})
                CREATE (e:Event {year: event.year,month:event.month,day:event.day})
                CREATE (e)-[:OCCURRED_IN]->(c)
                CREATE (e)-[:PERPETRATED_BY]->(g)
                CREATE (e)-[:USING]->(at)
                CREATE (e)-[:TARGETED]->(ta)
                """
                parm = {"events":events}
                session.run(query,parm)
            except Exception as e:
                print(e)

def insert_event(event:Dict[str,Dict[str,str]]):
    with driver.session() as session:
        query = """
                MATCH (c:Country {name:$event.country}),
                    (g:Group{name:$event.groups}),
                    (at:AttackType{type:$event.attack_type}),
                    (ta:TargetType{type:$event.target_type})
                CREATE (e:Event {year: $event.year,month:$event.month,day:$event.day})
                CREATE (e)-[:OCCURRED_IN]->(c)
                CREATE (e)-[:PERPETRATED_BY]->(g)
                CREATE (e)-[:USING]->(at)
                CREATE (e)-[:TARGETED]->(ta)
                """
        params = {"event":event}
        res = Maybe.from_optional(session.run(query,params).single())
        return res