from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/showtimes",
    tags=["Showtimes"]
)


@router.post("/", response_model=schemas.ShowtimeResponse)
def create_showtime(
    showtime: schemas.ShowtimeCreate,
    db: Session = Depends(get_db)
):
    new_showtime = models.Showtime(**showtime.model_dump())

    db.add(new_showtime)
    db.commit()
    db.refresh(new_showtime)

    return new_showtime


@router.get("/", response_model=list[schemas.ShowtimeResponse])
def get_showtimes(db: Session = Depends(get_db)):
    showtimes = db.query(models.Showtime).all()
    return showtimes


@router.get("/{showtime_id}", response_model=schemas.ShowtimeResponse)
def get_showtime(
    showtime_id: int,
    db: Session = Depends(get_db)
):
    showtime = db.query(models.Showtime).filter(
        models.Showtime.id == showtime_id
    ).first()

    if not showtime:
        raise HTTPException(
            status_code=404,
            detail="Función no encontrada"
        )

    return showtime


@router.get("/movie/{movie_api_id}", response_model=list[schemas.ShowtimeResponse])
def get_showtimes_by_movie(
    movie_api_id: int,
    db: Session = Depends(get_db)
):
    showtimes = db.query(models.Showtime).filter(
        models.Showtime.movie_api_id == movie_api_id
    ).all()

    return showtimes