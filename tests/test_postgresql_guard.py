import pytest
from sqlalchemy import create_engine

from fullmetalcopy.drivers import require_postgresql


def test_require_postgresql_rejects_sqlite() -> None:
    engine = create_engine("sqlite:///:memory:")
    with engine.connect() as conn, pytest.raises(ValueError, match="only supports PostgreSQL"):
        require_postgresql(conn)
