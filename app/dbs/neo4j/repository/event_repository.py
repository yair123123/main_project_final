import math
from typing import List, Dict

from returns.maybe import Maybe

from app.settings.config_dbs import driver

def insert_many_events(all_events: List[Dict[str, Dict[str, str]]]):
    with driver.session() as session:
        try:
            query = """
                UNWIND $events AS event
                UNWIND event.groups AS group_name
                MATCH (c:City {name: event.city}),
                      (at:AttackedType {type: event.attack_type}),
                      (ta:TargetType {type: event.target_type})
                MERGE (g:Group {name: group_name})
                CREATE (e:Event {year: event.year, month: event.month, day: event.day})
                CREATE (e)-[:OCCURRED_IN]->(c)
                CREATE (e)-[:USING]->(at)
                CREATE (e)-[:TARGETED]->(ta)
                CREATE (e)-[:PERPETRATED_BY]->(g)
                RETURN e
            """
            parm = {"events": all_events}
            result = session.run(query, parm)
            created_events = [record["e"] for record in result]
            if not created_events:
                print("No events were created.")
            else:
                print(f"Created {len(created_events)} events.")
        except Exception as e:
            print(f"Error: {e}")
