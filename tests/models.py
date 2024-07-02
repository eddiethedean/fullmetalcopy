from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass

class XY(Base):
    __tablename__: str = "xy"
    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[str] = mapped_column(String(30))
    y: Mapped[int] = mapped_column(Integer)