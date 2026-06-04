from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/seats",
    tags=["Seats"]
)


@router.post("/", response_model=schemas.SeatResponse)
def create_seat(
    seat: schemas.SeatCreate,
    db: Session = Depends(get_db)
):
    new_seat = models.Seat(**seat.model_dump())

    try:
        db.add(new_seat)
        db.commit()
        db.refresh(new_seat)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ya existe un asiento con esa etiqueta o posición en esa sala"
        )

    return new_seat


@router.get("/", response_model=list[schemas.SeatResponse])
def get_seats(db: Session = Depends(get_db)):
    seats = db.query(models.Seat).order_by(
        models.Seat.room,
        models.Seat.y_position,
        models.Seat.x_position
    ).all()

    return seats


@router.get("/room/{room}", response_model=list[schemas.SeatResponse])
def get_seats_by_room(
    room: str,
    db: Session = Depends(get_db)
):
    seats = db.query(models.Seat).filter(
        models.Seat.room == room
    ).order_by(
        models.Seat.y_position,
        models.Seat.x_position
    ).all()

    return seats


@router.get("/{seat_id}", response_model=schemas.SeatResponse)
def get_seat(
    seat_id: int,
    db: Session = Depends(get_db)
):
    seat = db.query(models.Seat).filter(
        models.Seat.id == seat_id
    ).first()

    if not seat:
        raise HTTPException(
            status_code=404,
            detail="Asiento no encontrado"
        )

    return seat