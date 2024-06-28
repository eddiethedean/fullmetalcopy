# fullmetalcopy: simple functions for faster PostgreSQL bulk inserts

## What is it?

**fullmetalcopy** is a Python package with simple functions for faster PostgreSQL bulk inserts by copying to table.

## Main Features
Here are just a few of the things that fullmetalcopy does:

  - Choice of psycopg, psycopg2, or asyncpg driver
  - Copy csv to table
  - Copy Pandas DataFrame to table
  - Copy Polars DataFrame to table
  - Async (psycopg or asyncpg) and Sync (psycopg or psycopg2) functions

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/eddiethedean/fullmetalcopy

```sh
# PyPI
pip install fullmetalcopy

# install with a PostgreSQL driver
pip install fullmetalcopy[psycopg]
pip install fullmetalcopy[psycopg2]
pip install fullmetalcopy[asyncpg]

# install with a PostgreSQL driver and pandas/polars
pip install fullmetalcopy[psycopg, pandas]
pip install fullmetalcopy[asyncpg, polars]
```

## Dependencies
- [sqlalchemy](https://pypi.org/project/SQLAlchemy/)

## Optional Dependencies
- [psycopg](https://www.psycopg.org/psycopg3/)
- [psycopg2](https://www.psycopg.org/docs/)
- [asyncpg](https://magicstack.github.io/asyncpg/current/)
- [polars](https://pola.rs)
- [pandas](https://pandas.pydata.org/)

# Example code
```sh
import sqlalchemy as sa
import fullmetalcopy as fc

engine = sa.create_engine('postgresql+pyscopg2://scott:tiger@hostname/dbname')

# Copy CSV directly to database table
with open('data.csv', 'r') as csv_f:
    with engine.connect() as connection:
        fc.copy_csv(csv_f, 'table_name', 'table_name_temp', connection, schema='test')
        connection.commit()
```