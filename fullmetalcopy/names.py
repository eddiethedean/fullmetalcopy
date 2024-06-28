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
        with _io.TextIOWrapper(csv_file, encoding='utf-8') as text_file:
            first_line: str = text_file.readline().strip()
        if columns is None:
            column_names = first_line.split(sep)
        else:
            column_names = columns
    else:
        column_names = columns
    if schema:
        table_name = f'{schema}.{table_name}'
    return table_name, column_names