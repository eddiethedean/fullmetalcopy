import io

import pytest
import testing.postgresql
from sqlalchemy import Engine, create_engine, select, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from fullmetalcopy.asynchronous.copycsv import copy_from_csv as async_copy_from_csv
from fullmetalcopy.synchronous.copycsv import copy_from_csv
from tests.drivers import add_driver
from tests.models import XY, Base
from tests.write_csv import write_csv


def _create_app_xy(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS app"))
        conn.execute(text("DROP TABLE IF EXISTS app.xy CASCADE"))
        conn.execute(
            text(
                "CREATE TABLE app.xy (id INTEGER PRIMARY KEY, "
                "x VARCHAR(30) NOT NULL, y INTEGER NOT NULL)"
            )
        )


def test_copy_schema_pg3_sync() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        url: str = add_driver(postgresql.url(), "psycopg")
        engine: Engine = create_engine(url)
        _create_app_xy(engine)
        with engine.connect() as connection:
            with io.BytesIO() as csv_file:
                write_csv(csv_file)
                copy_from_csv(connection, csv_file, "xy", schema="app")
            connection.commit()

            rows = connection.execute(text("SELECT id, x, y FROM app.xy ORDER BY id")).fetchall()
            assert list(rows) == [(1, "a", 33), (2, "b", 66)]


def test_copy_schema_pg2() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        url: str = add_driver(postgresql.url(), "psycopg2")
        engine: Engine = create_engine(url)
        _create_app_xy(engine)
        with engine.connect() as connection:
            with io.BytesIO() as csv_file:
                write_csv(csv_file)
                copy_from_csv(connection, csv_file, "xy", schema="app")
            connection.commit()

            rows = connection.execute(text("SELECT id, x, y FROM app.xy ORDER BY id")).fetchall()
            assert list(rows) == [(1, "a", 33), (2, "b", 66)]


def test_pg3_explicit_columns_with_headers() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        url: str = add_driver(postgresql.url(), "psycopg")
        engine: Engine = create_engine(url)
        Base.metadata.create_all(engine)
        with engine.connect() as connection:
            with io.BytesIO() as csv_file:
                write_csv(csv_file)
                copy_from_csv(
                    connection,
                    csv_file,
                    "xy",
                    columns=["id", "x", "y"],
                    headers=True,
                )
            connection.commit()

            query = select(XY)
            results = connection.execute(query)
            assert list(results.fetchall()) == [(1, "a", 33), (2, "b", 66)]


@pytest.mark.asyncio
async def test_copy_schema_pg3_async() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        sync_engine = create_engine(postgresql.url())
        _create_app_xy(sync_engine)
        sync_engine.dispose()
        url: str = add_driver(postgresql.url(), "psycopg")
        engine: AsyncEngine = create_async_engine(url)
        try:
            async with engine.connect() as connection:
                with io.BytesIO() as csv_file:
                    write_csv(csv_file)
                    await async_copy_from_csv(connection, csv_file, "xy", schema="app")
                    await connection.commit()

                rows = (
                    await connection.execute(text("SELECT id, x, y FROM app.xy ORDER BY id"))
                ).fetchall()
                assert list(rows) == [(1, "a", 33), (2, "b", 66)]
        finally:
            await engine.dispose()


@pytest.mark.asyncio
async def test_asyncpg_headers_and_explicit_columns() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        Base.metadata.create_all(create_engine(postgresql.url()))
        url: str = add_driver(postgresql.url(), "asyncpg")
        engine: AsyncEngine = create_async_engine(url)
        try:
            async with engine.connect() as connection:
                with io.BytesIO() as csv_file:
                    write_csv(csv_file)
                    await async_copy_from_csv(
                        connection,
                        csv_file,
                        "xy",
                        columns=["id", "x", "y"],
                        headers=True,
                    )
                    await connection.commit()

                query = select(XY)
                results = await connection.execute(query)
                assert list(results.fetchall()) == [(1, "a", 33), (2, "b", 66)]
        finally:
            await engine.dispose()
