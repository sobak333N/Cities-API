from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float

from app.db.core import Base


class City(Base):
    __tablename__ = "city"

    city_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    latitude: Mapped[Float] = mapped_column(Float, nullable=False)
    longtitude: Mapped[Float] = mapped_column(Float, nullable=False)