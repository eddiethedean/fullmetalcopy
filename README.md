# fullmetalcopy

Small helpers for **fast PostgreSQL bulk loads**: stream CSV into a table using the server’s copy path, with **SQLAlchemy** sync or async connections.

## Features

- Works with **psycopg** (v3), **psycopg2**, or **asyncpg** (async only for the latter two with SQLAlchemy’s asyncio support).
- Sync and async entrypoints.
- Optional **pandas** / **polars** extras if you use those stacks alongside the same drivers.

## Install

```sh
pip install fullmetalcopy

# With a PostgreSQL driver
pip install "fullmetalcopy[psycopg]"
pip install "fullmetalcopy[psycopg2]"
pip install "fullmetalcopy[asyncpg]"

# With optional dataframe libraries
pip install "fullmetalcopy[psycopg,pandas]"
pip install "fullmetalcopy[asyncpg,polars]"
```

### Development

```sh
pip install -e ".[dev]"
ruff check .
mypy fullmetalcopy
pytest
```

## Dependencies

- **Required:** [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) 2.0+
- **Optional:** [psycopg](https://www.psycopg.org/psycopg3/), [psycopg2](https://www.psycopg.org/docs/), [asyncpg](https://magicstack.github.io/asyncpg/), [pandas](https://pandas.pydata.org/), [polars](https://pola.rs/)

## Usage

### Synchronous (`psycopg` or `psycopg2`)

```python
import io

import sqlalchemy as sa

import fullmetalcopy as fc

engine = sa.create_engine("postgresql+psycopg2://scott:tiger@hostname/dbname")

with io.BytesIO() as buf:
    buf.write(b"id,name\n1,Ada\n")
    buf.seek(0)
    with engine.connect() as conn:
        fc.copy_from_csv(conn, buf, "people")
        conn.commit()
```

### Asynchronous (`asyncpg` or `psycopg`)

```python
import io

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine

import fullmetalcopy as fc

async def main() -> None:
    engine = create_async_engine("postgresql+asyncpg://scott:tiger@hostname/dbname")
    try:
        async with engine.connect() as conn:
            with io.BytesIO() as buf:
                buf.write(b"id,name\n1,Ada\n")
                buf.seek(0)
                await fc.async_copy_from_csv(conn, buf, "people")
                await conn.commit()
    finally:
        await engine.dispose()
```

`copy_from_csv` / `async_copy_from_csv` accept the same keyword options (`sep`, `null`, `columns`, `headers`, `schema`) as the underlying implementations; see the docstrings in `fullmetalcopy.synchronous.copycsv` and `fullmetalcopy.asynchronous.copycsv`.

## Project links

- Source: [github.com/eddiethedean/fullmetalcopy](https://github.com/eddiethedean/fullmetalcopy)
