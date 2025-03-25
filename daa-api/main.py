from fastapi import FastAPI
from app.routes import staff, patient, appointment
from app.database import create_db_and_tables, populate_tables

API_PREFIX = "/api/v0"
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    populate_tables()

app.include_router(staff.router, prefix=API_PREFIX)
app.include_router(patient.router, prefix=API_PREFIX)
app.include_router(appointment.router, prefix=API_PREFIX)