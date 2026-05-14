# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0]

### Added

- `require_postgresql()` guard and clearer errors for non-PostgreSQL SQLAlchemy dialects.
- Regression tests for schema-qualified copies, asyncpg header/column parity, and the PostgreSQL guard.
- Expanded README (API table, driver matrix, examples).

### Changed

- **Packaging:** PEP 621 metadata in `pyproject.toml`, setuptools 77+, wheel and sdist without vendored tests.
- **Typing:** public and internal copy helpers use `typing.BinaryIO` instead of `io.BytesIO` only.
- **CSV / names:** header line decoded as UTF-8 and parsed with `csv.reader`; `adapt_names` no longer folds `schema` into the table string.

### Fixed

- **Psycopg3:** `COPY` target for `schema=` is built as two SQL identifiers (`schema.table`), not a single quoted `"schema.table"` name.
- **Psycopg2:** schema targeting uses `SET LOCAL search_path` and an unqualified table name (reliable with `copy_from`).
- **Asyncpg:** shared `adapt_names` header handling; `copy_to_table` is always called with `header=False` after a header line is consumed so the first data row is not skipped twice.

### Development

- Ruff, Mypy, pytest (with coverage defaults), and GitHub Actions CI (Python 3.10 and 3.12, PostgreSQL packages for tests).

## [0.1.0]

Initial published API: synchronous and asynchronous CSV copy helpers for PostgreSQL via SQLAlchemy.
