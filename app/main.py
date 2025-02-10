import time
from typing import Annotated
import zoneinfo
from datetime import datetime
from fastapi import Depends, FastAPI,HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from models import Customer, Invoice
from db import create_all_tables
from .routers import customers, transactions, invoices, plans


app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

@app.middleware("http") #le pasamos el tipo que en este caso es http
async def log_request_time(request: Request, call_next):
    start_time = time.time() #este start_time es justo antes de que se empiece a procesar el request
    response = await call_next(request) #como es una función asyncrona debemos poner el await
    process_time = time.time() - start_time # con esto calculamos lo que se demoro la línea anterior en ejecutarse
    print(f"Request: {request.url} completed in: {process_time:.4f} seconds")
    return response

security = HTTPBasic()

@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]): # To tell FastAPI that this is an endpoint, we need a decorator
    print(credentials)
    if credentials.username == "lcmartinez" and credentials.password == "query":
        return {"message": f"hola {credentials.username}!"}
    else:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED)

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}
@app.get("/time/{iso_code}")
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()   
    timezone_str =  country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)


    return {"time": datetime.now(tz)}

@app.get("/timef/{format}")
async def get_current_time(format: str):
    if format not in ["12", "24"]:
        raise HTTPException(status_code=400, detail="Invalid format. Use '12' or '24'.")
    now = datetime.now()

    if format == "12":
        time_str = now.strftime("%I:%M:%S %p")  # 12-hour format
    else:
        time_str = now.strftime("%H:%M:%S")     # 24-hour format

    return {"time": time_str, "format": f"{format}-hour"}



db_customers: list[Customer] = []




