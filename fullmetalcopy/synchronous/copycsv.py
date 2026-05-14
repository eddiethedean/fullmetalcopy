from typing import BinaryIO

import sqlalchemy as _sa

import fullmetalcopy.drivers as _drivers


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
    Copy CSV bytes from ``csv_file`` into a PostgreSQL table.

    ``csv_file`` must be binary-mode (e.g. ``io.BytesIO`` or ``open(..., \"rb\")``).

    ``null`` is passed to the active driver. On the **psycopg3** implementation, each
    cell that compares equal to ``null`` is sent as SQL NULL; the default ``\"\"`` maps
    empty fields to NULL.

    ``schema`` sets the PostgreSQL schema for the target table (``search_path`` is not changed).

    Example
    -------
    import sqlalchemy as sa
    from fullmetalcopy.synchronous.copycsv import copy_from_csv

    engine = sa.create_engine('postgresql+psycopg://user:password@host:port/dbname')
    with engine.connect() as connection:
        with open("people.csv", "rb") as csv_file:
            copy_from_csv(connection, csv_file, 'people')
        connection.commit()
    """
    _drivers.require_postgresql(connection)
    driver: str = _drivers.connection_driver_name(connection)

    if driver == "psycopg":
        import fullmetalcopy.synchronous.pg3.copycsv as _pg3_copy

        _pg3_copy.copy_from_csv(
            connection, csv_file, table_name, sep, null, columns, headers, schema
        )
    elif driver == "psycopg2":
        import fullmetalcopy.synchronous.pg2.copycsv as _pg2_copy

        _pg2_copy.copy_from_csv(
            connection, csv_file, table_name, sep, null, columns, headers, schema
        )
    else:
        raise ValueError("driver must be psycopg or psycopg2")
