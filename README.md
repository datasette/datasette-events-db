# datasette-events-db

[![PyPI](https://img.shields.io/pypi/v/datasette-events-db.svg)](https://pypi.org/project/datasette-events-db/)
[![Changelog](https://img.shields.io/github/v/release/simonw/datasette-events-db?include_prereleases&label=changelog)](https://github.com/simonw/datasette-events-db/releases)
[![Tests](https://github.com/simonw/datasette-events-db/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/datasette-events-db/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-events-db/blob/main/LICENSE)

Log Datasette events to a database table

## Installation

Install this plugin in the same environment as Datasette.
```bash
datasette install datasette-events-db
```
## Usage

Once installed, all [Datasette events](https://docs.datasette.io/en/latest/events.html) will be logged to a table called `datasette_events`. This table will be created in the `_internal` database, but can be moved to another database using the following plugin configuration option:

```yaml
plugins:
  datasette-events-db:
    database: my_database
```

The table will be created when Datasette starts up, if it does not already exist.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd datasette-events-db
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
