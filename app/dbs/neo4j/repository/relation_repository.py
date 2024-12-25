import pandas as pd
from pandas import DataFrame
from returns.maybe import Maybe

from app.dbs.mongodb.repository import get_point_by_region, get_point_by_country
from app.settings.config_dbs import driver


def groups_with_common_goal_by_country():
    with driver.session() as session:
        query = """
            MATCH (region:Country) <-[:IN]- (c:City)<-[:OCCURRED_IN]-(event:Event)-[:TARGETED]->(target:TargetType)
            MATCH (event)-[:PERPETRATED_BY]->(group:Group)
            WITH region.name AS Region,
                 target.type AS Target,
                 COLLECT(DISTINCT group.name) AS Groups
            WITH Region, Target, Groups, SIZE(Groups) AS GroupCount
            ORDER BY Region, GroupCount DESC
            WITH Region, COLLECT({Target: Target, Groups: Groups, GroupCount: GroupCount}) AS TargetGroups
            RETURN Region, TargetGroups[0] AS MostAttackedTarget
            """
        res = Maybe.from_optional(session.run(query).data()).value_or([])
        return [{"location": get_point_by_country(x.get("Region")),
                 "groups": x.get("MostAttackedTarget", {}).get("Groups", [])} for x
                in res]


def groups_with_common_goal_by_region():
    with driver.session() as session:
        query = """
        MATCH (region:Region)<-[:IN]- (o:Country) <-[:IN]- (c:City)<-[:OCCURRED_IN]-(event:Event)-[:TARGETED]->(target:TargetType)
        MATCH (event)-[:PERPETRATED_BY]->(group:Group)
        WITH region.name AS Region,
             target.type AS Target,
             COLLECT(DISTINCT group.name) AS Groups
        WITH Region, Target, Groups, SIZE(Groups) AS GroupCount
        ORDER BY Region, GroupCount DESC
        WITH Region, COLLECT({Target: Target, Groups: Groups, GroupCount: GroupCount}) AS TargetGroups
        RETURN Region, TargetGroups[0] AS MostAttackedTarget

            """
        res = Maybe.from_optional(session.run(query).data()).value_or([])

    return [
        {"location": get_point_by_region(x.get("Region")), "groups": x.get("MostAttackedTarget", {}).get("Groups", [])}
        for x in res]


def unique_groups_by_region():
    with driver.session() as session:
        query = """
        MATCH (g:Group) <- [:PERPETRATED_BY] - (e:Event) - [:OCCURRED_IN] - (c:City) - [:IN] - (o:Country) - [:IN] -  (r:Region)
        return r.name as region ,COLLECT(DISTINCT g.name) as groups , COUNT(DISTINCT g) as group_count
        """
        res = Maybe.from_optional(session.run(query).data()).value_or([])

    return [
        {"location": get_point_by_region(x.get("region")), "groups": x.get("groups", []),
         "count": x.get("group_count", 0)}
        for x in res]


def unique_groups_by_country():
    with driver.session() as session:
        query = """
        MATCH (g:Group) <- [:PERPETRATED_BY] - (e:Event) - [:OCCURRED_IN] - (c:City) - [:IN] - (o:Country) - [:IN] -  (r:Region)
        return o.name as region ,COLLECT(DISTINCT g.name) as groups , COUNT(DISTINCT g) as group_count
        """
        res = Maybe.from_optional(session.run(query).data()).value_or([])

    return [
        {"location":get_point_by_country(x.get("region")), "groups": x.get("groups", []),
         "count": x.get("group_count", 0)}
        for x in res]


def shared_goals_in_groups_by_year(year):
    with driver.session() as session:
        query = """
        match (g:TargetType) <- [:TARGETED] - (e:Event{year: $year})
        match (g1:Group) - [:PERPETRATED_BY] - (e)
        return g.type as target_type, collect(DISTINCT g1.name) as groups, count(DISTINCT g1) as groups_count
        """
        return Maybe.from_optional(session.run(query, parameters={"year": int(year)}).data()).value_or([])


def shared_attack_type_in_groups_by_region():
    with driver.session() as session:
        query = """
        MATCH (region:Region)<-[:IN]-(country:Country)<-[:IN]-(city:City) <- [:OCCURRED_IN] - (event:Event)-[:PERPETRATED_BY]->(group:Group)
        MATCH (event) - [:USING] -> (attack_type:AttackedType)
        return region.name as region,attack_type.type as type,COUNT(Distinct group.name) as count
        """
        res = Maybe.from_optional(session.run(query).data()).value_or([])
        df = pd.DataFrame(res)
        df_max: DataFrame = df.loc[df.groupby('region')['count'].idxmax()]
    return   [
            {"location":get_point_by_region(x["region"]), "type": x["type"],
             "count": x["count"]}
            for _,x in df_max.iterrows()]


def shared_attack_type_in_groups_by_country():
    with driver.session() as session:
        query = """
        MATCH (country:Country)<-[:IN]-(city:City) <- [:OCCURRED_IN] - (event:Event)-[:PERPETRATED_BY]->(group:Group)
        MATCH (event) - [:USING] -> (attack_type:AttackedType)
        return country.name as region,attack_type.type as type,COUNT(Distinct group.name) as count
        """
        res = Maybe.from_optional(session.run(query).data()).value_or([])
        df = pd.DataFrame(res)
        df_max: DataFrame = df.loc[df.groupby('region')['count'].idxmax()]

        res = [
            {"location":get_point_by_country(x["region"]), "type": x["type"],
             "count": x["count"]}
            for _,x in df_max.iterrows()]
    return res
