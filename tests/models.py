from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class XY(Base):
    __tablename__: str = "xy"
    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[str] = mapped_column(String(30))
    y: Mapped[int] = mapped_column(Integer)
