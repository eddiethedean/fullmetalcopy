import typing as _t

import psycopg as _psycopg
import sqlalchemy as _sa
import sqlalchemy.ext.asyncio as _sa_asyncio


async def get_driver_connection(
    async_connection: _sa_asyncio.AsyncConnection,
) -> _psycopg.AsyncConnection:
    raw_connection: _sa.PoolProxiedConnection = await async_connection.get_raw_connection()
    return _t.cast(_psycopg.AsyncConnection, raw_connection.driver_connection)
