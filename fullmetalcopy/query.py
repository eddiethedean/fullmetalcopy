from __future__ import annotations


def create_copy_query(table_name: str, fields: list[str], schema: str | None = None):
    import psycopg.sql as _sql

    table_ref = (
        _sql.SQL(".").join([_sql.Identifier(schema), _sql.Identifier(table_name)])
        if schema
        else _sql.Identifier(table_name)
    )
    return _sql.SQL("COPY {table} ({fields}) FROM STDOUT").format(
        fields=_sql.SQL(",").join([_sql.Identifier(col) for col in fields]),
        table=table_ref,
    )
