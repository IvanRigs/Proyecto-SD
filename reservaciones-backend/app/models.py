from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Showtime(Base):
    __tablename__ = "showtimes"

    id = Column(Integer, primary_key=True, index=True)

    # ID de la película que viene de la API externa
    movie_api_id = Column(Integer, nullable=False)

    # Guardamos el título solo como referencia
    movie_title = Column(String, nullable=True)

    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    room = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="showtime")


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    row = Column(String, nullable=False)
    number = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("row", "number", name="unique_seat_row_number"),
    )


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)

    user_name = Column(String, nullable=False)

    showtime_id = Column(Integer, ForeignKey("showtimes.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)

    status = Column(String, default="active")

    showtime = relationship("Showtime", back_populates="reservations")
    seat = relationship("Seat")

    __table_args__ = (
        UniqueConstraint(
            "showtime_id",
            "seat_id",
            "status",
            name="unique_active_reservation"
        ),
    )