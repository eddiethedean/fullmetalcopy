import csv
import io as _io


def adapt_names(
    csv_file,
    table_name: str,
    sep: str,
    columns: list[str] | None,
    headers: bool,
) -> tuple[str, list[str] | None]:
    """Read optional header row for column names; advance ``csv_file`` past the header when present.

    Does not qualify the table with ``schema`` (callers pass schema to the driver or SQL builder).
    """
    column_names: list[str] | None
    if headers:
        b_first_line: bytes = csv_file.readline()
        if not b_first_line:
            raise ValueError("CSV is empty but headers was True")
        first_line: str = b_first_line.decode("utf-8").strip()
        if not first_line:
            raise ValueError("CSV header line is empty")
        if columns is None:
            column_names = list(next(csv.reader(_io.StringIO(first_line), delimiter=sep)))
        else:
            column_names = columns
    else:
        column_names = columns
    return table_name, column_names
