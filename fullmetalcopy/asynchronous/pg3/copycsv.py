import csv as _csv
import io as _io

import psycopg as _psycopg
import psycopg.sql as _sql
import sqlalchemy.ext.asyncio as _sa_asyncio

import fullmetalcopy.asynchronous.pg3.connection as _connection
import fullmetalcopy.names as _names
import fullmetalcopy.query as _query


async def copy_from_csv(
    async_connection: _sa_asyncio.AsyncConnection,
    csv_file: _io.BytesIO,
    table_name: str,
    sep: str = ",",
    null: str = "",
    columns: list[str] | None = None,
    headers: bool = True,
    schema: str | None = None,
) -> None:
    """
    Copy CSV file to PostgreSQL table.

    Example
    -------
    >>> from sqlalchemy.ext.asyncio import create_async_engine
    >>> from fullmetalcopy.asynchronous.pg3.copycsv import copy_from_csv

    >>> async_engine = sa.create_async_engine('postgresql+psycopg://user:password@host:port/dbname')
    >>> async with async_engine.connect() as async_connection:
    ...     with open("people.csv", "rb") as csv_file:
    ...         await copy_from_csv(async_connection, csv_file, 'people')
    ...     await async_connection.commit()

    >>> await async_engine.dispose()
    """
    table_name, column_names = _names.adapt_names(
        csv_file, table_name, sep, columns, headers, schema
    )
    if column_names is None:
        raise ValueError("columns must be provided when headers is False")
    query: _sql.Composed = _query.create_copy_query(table_name, column_names)
    pg3_async_connection: _psycopg.AsyncConnection
    pg3_async_connection = await _connection.get_driver_connection(async_connection)
    async with pg3_async_connection.cursor() as async_cursor, async_cursor.copy(query) as copy:
        with _io.TextIOWrapper(csv_file, encoding="utf-8") as text_file:
            for row in _csv.reader(text_file):
                values: list[str | None] = [None if val == null else val for val in row]
                await copy.write_row(values)
