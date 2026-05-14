import sqlalchemy as _sa
import sqlalchemy.ext.asyncio as _sa_asyncio


def connection_driver_name(
    connection: _sa.engine.base.Connection | _sa_asyncio.AsyncConnection,
) -> str:
    return connection.dialect.driver
