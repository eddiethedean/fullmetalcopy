import typing as _t
import io as _io


def adapt_names(
    csv_file,
    table_name: str,
    sep: str,
    columns: _t.Optional[list[str]],
    headers: bool,
    schema: _t.Optional[str]
) -> tuple[str, list[str] | None]:
    column_names: list[str] | None
    if headers:
        b_first_line: bytes = csv_file.readline()
        first_line: str = b_first_line.decode().strip()
        if columns is None:
            column_names = first_line.split(sep)
        else:
            column_names = columns
    else:
        column_names = columns
    if schema:
        table_name = f'{schema}.{table_name}'
    return table_name, column_names