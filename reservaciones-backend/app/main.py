from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socket
import os

from app.database import Base, engine
from app.routes import showtimes, seats, reservations

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Reservaciones Distribuido",
    description="Backend para proyecto final de Sistemas Distribuidos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(showtimes.router)
app.include_router(seats.router)
app.include_router(reservations.router)


@app.get("/")
def home():
    return {
        "message": "Backend de reservaciones funcionando"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "reservaciones-backend"
    }


@app.get("/node-info")
def node_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    return {
        "node": os.getenv("NODE_NAME", "backend-node-1"),
        "hostname": hostname,
        "ip": ip_address,
        "service": "reservaciones-api",
        "status": "running"
    }