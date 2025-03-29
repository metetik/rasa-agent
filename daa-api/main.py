from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import staff, patient, appointment
from app.database import create_db_and_tables, populate_tables, drop_tables

API_PREFIX = "/api/v0"
STATIC_PATH = "static"


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    populate_tables()


@app.on_event("shutdown")
async def shutdown_event():
    drop_tables()

app.mount(f"/{STATIC_PATH}", StaticFiles(directory=STATIC_PATH, html=True), name="static")

app.include_router(staff.router, prefix=API_PREFIX)
app.include_router(patient.router, prefix=API_PREFIX)
app.include_router(appointment.router, prefix=API_PREFIX)