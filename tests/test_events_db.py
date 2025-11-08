from datasette.app import Datasette
import json
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("configured_database", (None, "demo"))
async def test_log_events_to_db(configured_database):
    config = {
        "permissions": {"create-table": True},
    }
    if configured_database:
        config["plugins"] = {"datasette-events-db": {"database": configured_database}}

    expected_database = configured_database or "_internal"
    datasette = Datasette(
        memory=True,
        config=config,
    )
    db = datasette.add_memory_database("demo")
    await datasette.invoke_startup()
    # Drop table if it exists
    await db.execute_write("drop table if exists new_table")

    # Ensure we can see _internal if necessary
    if expected_database == "_internal":
        internal_db = datasette.get_internal_database()
        datasette.add_database(internal_db, name="_internal", route="_internal")

    # Test table was created and starts empty
    response = await datasette.client.get(
        f"/{expected_database}/datasette_events.json?_extra=columns"
    )
    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "next": None,
        "columns": [
            "id",
            "event",
            "created",
            "actor_id",
            "database_name",
            "table_name",
            "properties",
        ],
        "rows": [],
        "truncated": False,
    }
    # Now create a table via the Datasette API
    await datasette.client.post(
        "/demo/-/create",
        json={
            "table": "new_table",
            "columns": [
                {"name": "id", "type": "integer"},
                {"name": "name", "type": "text"},
            ],
            "pk": "id",
        },
    )
    # Should have recorded an event
    response2 = await datasette.client.get(
        f"/{expected_database}/datasette_events.json"
    )
    assert response2.status_code == 200
    rows = response2.json()["rows"]
    assert len(rows) == 1
    row = rows[0]
    assert row["event"] == "create-table"
    assert isinstance(row["created"], str)
    assert row["actor_id"] is None
    assert row["database_name"] == "demo"
    assert row["table_name"] == "new_table"
    props = json.loads(row["properties"])
    assert "schema" in props
