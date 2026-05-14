import io as _io
from typing import BinaryIO

import psycopg2._psycopg as _psycopg
import psycopg2.sql as _psql
import sqlalchemy as _sa

import fullmetalcopy.names as _names
import fullmetalcopy.synchronous.pg2.connection as _connection


def copy_from_csv(
    connection: _sa.engine.base.Connection,
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

    When ``schema`` is set, ``SET LOCAL search_path`` is applied so ``copy_from`` can use
    the unqualified table name (psycopg2 rejects some qualified forms for ``COPY``).

    Example
    -------
    >>> import sqlalchemy as sa
    >>> from fullmetalcopy.synchronous.pg2.copycsv import copy_from_csv

    >>> engine = sa.create_engine('postgresql+psycopg2://user:password@host:port/dbname')
    >>> with engine.connect() as connection:
    ...     with open("people.csv", "rb") as csv_file:
    ...         copy_from_csv(connection, csv_file, 'people')
    ...     connection.commit()
    """
    table_name, column_names = _names.adapt_names(csv_file, table_name, sep, columns, headers)
    pg2_connection: _psycopg.connection = _connection.get_driver_connection(connection)
    cursor: _psycopg.cursor = pg2_connection.cursor()
    try:
        if schema:
            cursor.execute(
                _psql.SQL("SET LOCAL search_path TO {}, public").format(_psql.Identifier(schema))
            )
        with _io.TextIOWrapper(csv_file, encoding="utf-8") as text_file:
            cursor.copy_from(text_file, table_name, sep=sep, null=null, columns=column_names)
    finally:
        cursor.close()
