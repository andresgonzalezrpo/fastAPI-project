import zoneinfo
from datetime import datetime
from fastapi import FastAPI,HTTPException
from models import Customer, Transaction, Invoice, CustomerCreate
from db import SessionDep





app = FastAPI()

@app.get("/")
async def root(): # To tell FastAPI that this is an endpoint, we need a decorator
    return {"message": "hola, Andres!"}

country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}
@app.get("/time/{iso_code}")
async def time(iso_code: str):
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

@app.post('/customers', response_model=Customer) # esta en mayuscula por que es una recomendacion cuando se crea una API rest
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump()) #
    db_customers.append(customer)
    customer.id = len(db_customers)
    return customer

@app.get('/customers',response_model=list[Customer])
async def list_customer():
    return db_customers

@app.get('/get_customer/{id}',response_model=Customer)
async def get_customer(id : int):
    for customer in db_customers:
        if(customer.id == id):
            return customer
    return None



@app.post('/transactions') # esta en mayuscula por que es una recomendacion cuando se crea una API rest
async def create_transaction(transaction_data: Transaction):

    return transaction_data

@app.post('/invoices') # esta en mayuscula por que es una recomendacion cuando se crea una API rest
async def create_customer(invoice_data: Invoice):

    return invoice_data