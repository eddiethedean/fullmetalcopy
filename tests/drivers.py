from sqlalchemy.engine.url import make_url


def add_driver(url: str, driver: str) -> str:
    """Return ``url`` with the SQLAlchemy driver suffix inserted (e.g. ``postgresql+psycopg2``).

    Uses SQLAlchemy’s URL parser so passwords and hosts containing ``:`` are not broken.
    """
    u = make_url(url)
    dialect = u.drivername or "postgresql"
    if "+" in dialect:
        return str(u)
    return str(u.set(drivername=f"{dialect}+{driver}"))
