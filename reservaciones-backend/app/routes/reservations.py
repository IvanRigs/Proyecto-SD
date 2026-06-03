from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@router.post("/", response_model=schemas.ReservationResponse)
def create_reservation(
    reservation: schemas.ReservationCreate,
    db: Session = Depends(get_db)
):
    showtime = db.query(models.Showtime).filter(
        models.Showtime.id == reservation.showtime_id
    ).first()

    if not showtime:
        raise HTTPException(
            status_code=404,
            detail="La función no existe"
        )

    seat = db.query(models.Seat).filter(
        models.Seat.id == reservation.seat_id
    ).first()

    if not seat:
        raise HTTPException(
            status_code=404,
            detail="El asiento no existe"
        )

    existing_reservation = db.query(models.Reservation).filter(
        models.Reservation.showtime_id == reservation.showtime_id,
        models.Reservation.seat_id == reservation.seat_id,
        models.Reservation.status == "active"
    ).first()

    if existing_reservation:
        raise HTTPException(
            status_code=409,
            detail="Este asiento ya está reservado para esta función"
        )

    new_reservation = models.Reservation(**reservation.model_dump())

    try:
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Conflicto: el asiento ya fue reservado por otro usuario"
        )

    return new_reservation


@router.get("/", response_model=list[schemas.ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    reservations = db.query(models.Reservation).all()
    return reservations


@router.get("/{reservation_id}", response_model=schemas.ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    reservation = db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id
    ).first()

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservación no encontrada"
        )

    return reservation


@router.delete("/{reservation_id}")
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    reservation = db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id
    ).first()

    if not reservation:
        raise HTTPException(
            status_code=404,
            detail="Reservación no encontrada"
        )

    reservation.status = "cancelled"
    db.commit()

    return {
        "message": "Reservación cancelada correctamente",
        "reservation_id": reservation_id
    }


@router.get("/showtime/{showtime_id}", response_model=list[schemas.ReservationResponse])
def get_reservations_by_showtime(
    showtime_id: int,
    db: Session = Depends(get_db)
):
    reservations = db.query(models.Reservation).filter(
        models.Reservation.showtime_id == showtime_id,
        models.Reservation.status == "active"
    ).all()

    return reservations


@router.get("/showtime/{showtime_id}/seats", response_model=list[schemas.SeatAvailabilityResponse])
def get_seats_availability(
    showtime_id: int,
    db: Session = Depends(get_db)
):
    showtime = db.query(models.Showtime).filter(
        models.Showtime.id == showtime_id
    ).first()

    if not showtime:
        raise HTTPException(
            status_code=404,
            detail="La función no existe"
        )

    seats = db.query(models.Seat).order_by(
        models.Seat.row,
        models.Seat.number
    ).all()

    active_reservations = db.query(models.Reservation).filter(
        models.Reservation.showtime_id == showtime_id,
        models.Reservation.status == "active"
    ).all()

    reserved_seat_ids = {reservation.seat_id for reservation in active_reservations}

    result = []

    for seat in seats:
        result.append({
            "id": seat.id,
            "row": seat.row,
            "number": seat.number,
            "reserved": seat.id in reserved_seat_ids
        })

    return result