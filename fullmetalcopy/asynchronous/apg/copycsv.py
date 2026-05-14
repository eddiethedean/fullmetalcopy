from typing import BinaryIO

import asyncpg as _asyncpg
import sqlalchemy.ext.asyncio as _sa_asyncio

import fullmetalcopy.asynchronous.apg.connection as _connection
import fullmetalcopy.names as _names


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
    Copy CSV file to PostgreSQL table.

    ``adapt_names`` may skip the first line when ``headers`` is True; asyncpg is always
    called with ``header=False`` so it does not skip an extra line.

    Example
    -------
    >>> import sqlalchemy as sa
    >>> from sqlalchemy.ext.asyncio import create_async_engine
    >>> from fullmetalcopy.asynchronous.apg.copycsv import copy_from_csv

    >>> async_engine = sa.create_async_engine('postgresql+asyncpg://user:password@host:port/dbname')
    >>> async with async_engine.connect() as async_connection:
    ...     with open("people.csv", "rb") as csv_file:
    ...         await copy_from_csv(async_connection, csv_file, 'people')
    ...     await async_connection.commit()

    >>> await async_engine.dispose()
    """
    _, column_names = _names.adapt_names(csv_file, table_name, sep, columns, headers)
    apg_async_connection: _asyncpg.Connection
    apg_async_connection = await _connection.get_driver_connection(async_connection)
    await apg_async_connection.copy_to_table(
        table_name,
        source=csv_file,
        delimiter=sep,
        header=False,
        null=null,
        columns=column_names,
        schema_name=schema,
        format="csv",
    )
