from datasette import hookimpl
import json

CREATE_TABLE_SQL = """
create table if not exists datasette_events (
    id integer primary key,
    event text,
    created text,
    actor_id text,
    database_name text,
    table_name text,
    properties text -- JSON other properties
)
"""


@hookimpl
def startup(datasette):
    async def inner():
        db = get_database(datasette)
        await db.execute_write(CREATE_TABLE_SQL)

    return inner


@hookimpl
def track_event(datasette, event):
    async def inner():
        db = get_database(datasette)
        properties = event.properties()
        # pop off the database and table properties if they exist
        database_name = properties.pop("database", None)
        table_name = properties.pop("table", None)
        placeholders = []
        values = []
        # A ? for each value that is not None, null for the others
        placeholders.append("?")
        values.append(event.name)
        placeholders.append("?")
        values.append(event.created.isoformat())
        if event.actor:
            placeholders.append("?")
            values.append(event.actor.get("id"))
        else:
            placeholders.append("null")
        if database_name:
            placeholders.append("?")
            values.append(database_name)
        else:
            placeholders.append("null")
        if table_name:
            placeholders.append("?")
            values.append(table_name)
        else:
            placeholders.append("null")
        placeholders.append("?")
        values.append(json.dumps(properties))
        await db.execute_write(
            "insert into datasette_events (event, created, actor_id, database_name, table_name, properties) values ({})".format(
                ",".join(placeholders)
            ),
            values,
        )

    return inner


def get_database(datasette):
    config = datasette.plugin_config("datasette-events-db") or {}
    db_name = config.get("database")
    if not db_name:
        return datasette.get_internal_database()
    else:
        return datasette.get_database(db_name)
