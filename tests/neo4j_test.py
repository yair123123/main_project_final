import pytest

from app.dbs.neo4j.repository.groups_repository import insert_many_groups
from app.settings.config_dbs import driver


@pytest.fixture()
def clear_db():
    yield
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")

def test_insert_many_group():
    groups = {("el_kahida","hamas"),("hizballa","taliban")}
    insert_many_groups(groups)