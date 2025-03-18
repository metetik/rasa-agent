from fastapi import FastAPI
from app.routes import staff, patient
from app.database import create_db_and_tables, populate_tables

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    populate_tables()

app.include_router(staff.router, prefix="/api/v0")
app.include_router(patient.router, prefix="/api/v0")