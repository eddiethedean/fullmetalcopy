import io

import pytest
from sqlalchemy import create_engine, select
import testing.postgresql
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from fullmetalcopy.asynchronous.copycsv import copy_from_csv
from tests.drivers import add_driver
from tests.models import XY, Base
from tests.write_csv import write_csv


@pytest.mark.asyncio
async def test_simple_copy_apg() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        Base.metadata.create_all(create_engine(postgresql.url()))
        url: str = add_driver(postgresql.url(), 'asyncpg')
        engine: AsyncEngine = create_async_engine(url)
        async with engine.connect() as connection:
            with io.BytesIO() as csv_file:
                write_csv(csv_file)
                await copy_from_csv(connection, csv_file, 'xy')
                await connection.commit()

            query = select(XY)
            results = await connection.execute(query)
            assert list(results.fetchall()) == [(1, 'a', 33), (2, 'b', 66)]
    await engine.dispose()


@pytest.mark.asyncio
async def test_simple_copy_pg3() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        Base.metadata.create_all(create_engine(postgresql.url()))
        url: str = add_driver(postgresql.url(), 'psycopg')
        engine: AsyncEngine = create_async_engine(url)
        async with engine.connect() as connection:
            with io.BytesIO() as csv_file:
                write_csv(csv_file)
                await copy_from_csv(connection, csv_file, 'xy')
                await connection.commit()

            query = select(XY)
            results = await connection.execute(query)
            assert list(results.fetchall()) == [(1, 'a', 33), (2, 'b', 66)]
    await engine.dispose()