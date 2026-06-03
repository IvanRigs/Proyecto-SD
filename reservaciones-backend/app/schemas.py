from pydantic import BaseModel
from typing import Optional


class ShowtimeBase(BaseModel):
    movie_api_id: int
    movie_title: Optional[str] = None
    date: str
    time: str
    room: str


class ShowtimeCreate(ShowtimeBase):
    pass


class ShowtimeResponse(ShowtimeBase):
    id: int

    class Config:
        from_attributes = True


class SeatBase(BaseModel):
    row: str
    number: int


class SeatCreate(SeatBase):
    pass


class SeatResponse(SeatBase):
    id: int

    class Config:
        from_attributes = True


class ReservationCreate(BaseModel):
    user_name: str
    showtime_id: int
    seat_id: int


class ReservationResponse(BaseModel):
    id: int
    user_name: str
    showtime_id: int
    seat_id: int
    status: str

    class Config:
        from_attributes = True


class SeatAvailabilityResponse(BaseModel):
    id: int
    row: str
    number: int
    reserved: bool