from app.settings.config_dbs import elastic_client


def create_index(index_name):
    if not elastic_client.indices.exists(index=index_name):
        elastic_client.indices.create(index=index_name,body={
            "mappings": {
                "properties": {
                    "eventid": {"type":"text"},
                    "description": {"type":"text"},
                }
            }
        })

