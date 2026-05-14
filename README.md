# fullmetalcopy

**Fast PostgreSQL bulk loads from CSV** using the server-side copy path, wired through **SQLAlchemy 2** so you keep your normal engines and connection patterns.

PyPI: [fullmetalcopy](https://pypi.org/project/fullmetalcopy/) · Source: [GitHub](https://github.com/eddiethedean/fullmetalcopy)

---

## Why use this?

Bulk-inserting rows with plain `INSERT` is slow for large datasets. This library streams CSV bytes into a table via PostgreSQL’s efficient copy-style ingestion, with thin wrappers over **psycopg3**, **psycopg2**, or **asyncpg** depending on your SQLAlchemy URL.

---

## Requirements

| | |
| --- | --- |
| **Python** | 3.10+ |
| **Database** | PostgreSQL only (checked at runtime) |
| **Core** | [SQLAlchemy](https://pypi.org/project/SQLAlchemy/) ≥ 2.0 |

Install at least one driver extra (or bring your own compatible stack):

| Extra | Use case |
| --- | --- |
| `psycopg` | Sync or async with **psycopg** v3 (`postgresql+psycopg://…`, `postgresql+psycopg_async://…`) |
| `psycopg2` | Sync with **psycopg2** (`postgresql+psycopg2://…`) |
| `asyncpg` | Async with **asyncpg** (`postgresql+asyncpg://…`) |
| `pandas` / `polars` | Optional; same extras as declared in `pyproject.toml` if you combine with dataframe tooling |

---

## Install

```sh
pip install fullmetalcopy

# Drivers (pick what matches your engine URL)
pip install "fullmetalcopy[psycopg]"
pip install "fullmetalcopy[psycopg2]"
pip install "fullmetalcopy[asyncpg]"

# Examples with dataframe extras
pip install "fullmetalcopy[psycopg,pandas]"
pip install "fullmetalcopy[asyncpg,polars]"
```

---

## Public API

Import from the package root:

```python
import fullmetalcopy as fc

fc.__version__          # package version string
fc.copy_from_csv       # synchronous
fc.async_copy_from_csv  # asynchronous (alias of the async module’s copy_from_csv)
```

Both callables accept a **binary** CSV stream (`io.BytesIO`, `open(..., "rb")`, or any `typing.BinaryIO`).

| Argument | Default | Meaning |
| --- | --- | --- |
| `connection` / `async_connection` | — | SQLAlchemy `Connection` or `AsyncConnection` |
| `csv_file` | — | Binary stream positioned at the start of the CSV payload |
| `table_name` | — | Target table name (unqualified unless you use `schema`) |
| `sep` | `","` | Field delimiter |
| `null` | `""` | See [CSV and null semantics](#csv-and-null-semantics) below |
| `columns` | `None` | Optional explicit column list (order must match CSV columns after the header is applied) |
| `headers` | `True` | If `True`, the first line is treated as a header row and skipped from data (column names may still be taken from the file or from `columns`) |
| `schema` | `None` | PostgreSQL schema name; `search_path` is not permanently changed |

Driver is inferred from `connection.dialect.driver`. Non-PostgreSQL dialects raise a clear error.

---

## Usage examples

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

### Non-default schema

```python
fc.copy_from_csv(conn, buf, "invoices", schema="billing")
await fc.async_copy_from_csv(conn, buf, "invoices", schema="billing")
```

### Header row plus explicit column order

When the file has a header but you want to pin the column list (and skip the header line the same way on every backend):

```python
fc.copy_from_csv(
    conn,
    buf,
    "people",
    columns=["id", "name"],
    headers=True,
)
```

---

## Driver behavior (summary)

| Backend | Sync | Async | Notes |
| --- | --- | --- | --- |
| **psycopg** v3 | Yes | Yes | Rows are read with Python’s `csv` module and sent with `copy.write_row`; column count must match. |
| **psycopg2** | Yes | No | Uses `cursor.copy_from`. For `schema=…`, uses `SET LOCAL search_path` then an unqualified table name (reliable with `COPY`). |
| **asyncpg** | No | Yes | Uses `copy_to_table`. Header skipping is aligned with other backends (`adapt_names`); asyncpg is called with `header=False` after any header line is consumed. |

For full detail, see the docstrings in `fullmetalcopy.synchronous.copycsv` and `fullmetalcopy.asynchronous.copycsv`, and the per-driver modules under `fullmetalcopy.synchronous` / `fullmetalcopy.asynchronous`.

---

## CSV and null semantics

- The header line (when `headers=True`) is decoded as **UTF-8** and parsed with **`csv.reader`**, so quoted fields in the header are handled like normal CSV.
- On the **psycopg3** path, each data row is also read with **`csv.reader`** and must have exactly as many fields as the resolved column list, or a `ValueError` is raised.
- On the **psycopg3** path, any cell that **equals** the `null` string is stored as SQL `NULL`. The default `null=""` maps **empty** fields to `NULL`. If you need to keep empty strings as empty strings, set `null` to a sentinel that does not appear in real data (for example `"\N"` where appropriate).

PostgreSQL’s CSV rules and Python’s `csv` module are very close but not identical for exotic cases (embedded newlines, unusual escapes). For maximum fidelity on huge files, consider a raw server-side `COPY … FROM STDIN` pipeline; this library targets typical spreadsheet-style CSV.

---

## Development

From a clone of the repository:

```sh
pip install -e ".[dev]"
ruff format .
ruff check .
mypy fullmetalcopy
pytest
```

`[dev]` pulls all supported drivers, pytest, Ruff, Mypy, and `testing.postgresql` for the test suite.

---

## License

MIT — see [LICENSE](LICENSE).
