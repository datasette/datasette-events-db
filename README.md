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

Usage instructions go here.

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
