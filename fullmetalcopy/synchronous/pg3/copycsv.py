import csv as _csv
import io as _io

import psycopg.connection as _pg3_connection
import psycopg.cursor as _pg3_cursor
import psycopg.sql as _sql
import sqlalchemy as _sa

import fullmetalcopy.names as _names
import fullmetalcopy.query as _query
import fullmetalcopy.synchronous.pg3.connection as _connection


def copy_from_csv(
    connection: _sa.engine.base.Connection,
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
    import sqlalchemy as sa
    from fullmetalcopy.synchronous.pg3.copycsv import copy_from_csv

    engine = sa.create_engine('postgresql+psycopg://user:password@host:port/dbname')
    with engine.connect() as connection:
        with open("people.csv", "rb") as csv_file:
            copy_from_csv(connection, csv_file, 'people')
        connection.commit()
    """
    table_name, column_names = _names.adapt_names(
        csv_file, table_name, sep, columns, headers, schema
    )
    if column_names is None:
        raise ValueError("columns must be provided when headers is False")
    query: _sql.Composed = _query.create_copy_query(table_name, column_names)
    pg3_connection: _pg3_connection.Connection = _connection.get_driver_connection(connection)
    cursor: _pg3_cursor.Cursor = pg3_connection.cursor()
    with cursor.copy(query) as copy, _io.TextIOWrapper(csv_file, encoding="utf-8") as text_file:
        for row in _csv.reader(text_file):
            values: list[str | None] = [None if val == null else val for val in row]
            copy.write_row(values)
