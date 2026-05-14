import sqlalchemy as _sa
import sqlalchemy.ext.asyncio as _sa_asyncio


def connection_driver_name(
    connection: _sa.engine.base.Connection | _sa_asyncio.AsyncConnection,
) -> str:
    return connection.dialect.driver


def require_postgresql(
    connection: _sa.engine.base.Connection | _sa_asyncio.AsyncConnection,
) -> None:
    if connection.dialect.name != "postgresql":
        raise ValueError(
            "fullmetalcopy only supports PostgreSQL; "
            f"got dialect {connection.dialect.name!r} "
            f"(driver {connection.dialect.driver!r})"
        )
