from typing import BinaryIO

import sqlalchemy.ext.asyncio as _sa_asyncio

import fullmetalcopy.drivers as _drivers


async def copy_from_csv(
    async_connection: _sa_asyncio.AsyncConnection,
    csv_file: BinaryIO,
    table_name: str,
    sep: str = ",",
    null: str = "",
    columns: list[str] | None = None,
    headers: bool = True,
    schema: str | None = None,
) -> None:
    """
    Copy CSV bytes from ``csv_file`` into a PostgreSQL table (async).

    ``csv_file`` must be binary-mode (e.g. ``io.BytesIO`` or ``open(..., \"rb\")``).

    ``null`` is passed to the active driver. On the **psycopg3** implementation, each
    cell that compares equal to ``null`` is sent as SQL NULL; the default ``\"\"`` maps
    empty fields to NULL.

    ``schema`` sets the PostgreSQL schema for the target table.

    Example
    -------
    >>> from sqlalchemy.ext.asyncio import create_async_engine
    >>> from fullmetalcopy.asynchronous.copycsv import copy_from_csv

    >>> async_engine = create_async_engine('postgresql+asyncpg://user:password@host:port/dbname')
    >>> async with async_engine.connect() as async_connection:
    ...     with open("people.csv", "rb") as csv_file:
    ...         await copy_from_csv(async_connection, csv_file, 'people')
    ...     await async_connection.commit()

    >>> await async_engine.dispose()
    """
    _drivers.require_postgresql(async_connection)
    driver: str = _drivers.connection_driver_name(async_connection)
    if driver == "psycopg":
        import fullmetalcopy.asynchronous.pg3.copycsv as _pg3_copy

        await _pg3_copy.copy_from_csv(
            async_connection, csv_file, table_name, sep, null, columns, headers, schema
        )
    elif driver == "asyncpg":
        import fullmetalcopy.asynchronous.apg.copycsv as _apg_copy

        await _apg_copy.copy_from_csv(
            async_connection, csv_file, table_name, sep, null, columns, headers, schema
        )
    else:
        raise ValueError("driver must be psycopg or asyncpg")
