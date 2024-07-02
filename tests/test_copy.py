import testing.postgresql
import io

from sqlalchemy import Engine, create_engine, select
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from fullmetalcopy.synchronous.copycsv import copy_from_csv


class Base(DeclarativeBase):
    pass

class XY(Base):
    __tablename__ = "xy"
    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[str] = mapped_column(String(30))
    y: Mapped[int] = mapped_column(Integer)


def write_csv(csv_file: io.BytesIO) -> None:
    csv_file.writelines([
        b'id,x,y\n',
        b'1,a,33\n',
        b'2,b,66\n'
    ])
    csv_file.seek(0)


def test_simple_copy() -> None:
    with testing.postgresql.Postgresql() as postgresql:
        print(postgresql.url())
        engine: Engine = create_engine(postgresql.url())
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
    test_simple_copy()