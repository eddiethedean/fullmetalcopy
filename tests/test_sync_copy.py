import testing.postgresql
import io

from sqlalchemy import Engine, create_engine, select

from fullmetalcopy.synchronous.copycsv import copy_from_csv
from tests.models import XY, Base
from tests.write_csv import write_csv
from tests.drivers import add_driver


def test_simple_copy_pg3() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        url: str = add_driver(postgresql.url(), 'psycopg')
        engine: Engine = create_engine(url)
        Base.metadata.create_all(engine)
        with engine.connect() as connection:
            with io.BytesIO() as csv_file:
                write_csv(csv_file)
                copy_from_csv(connection, csv_file, 'xy')
            connection.commit()

            query = select(XY)
            results = connection.execute(query)
            assert list(results.fetchall()) == [(1, 'a', 33), (2, 'b', 66)]


def test_simple_copy_pg2() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        url: str = add_driver(postgresql.url(), 'psycopg2')
        engine: Engine = create_engine(url)
        Base.metadata.create_all(engine)
        with engine.connect() as connection:
            with io.BytesIO() as csv_file:
                write_csv(csv_file)
                copy_from_csv(connection, csv_file, 'xy')
            connection.commit()

            query = select(XY)
            results = connection.execute(query)
            assert list(results.fetchall()) == [(1, 'a', 33), (2, 'b', 66)]


if __name__ == '__main__':
    test_simple_copy_pg2()