from fastapi import APIRouter
from models import Invoice

router = APIRouter()

@router.post('/invoices', tags=['invoices']) # esta en mayuscula por que es una recomendacion cuando se crea una API rest
async def create_customer(invoice_data: Invoice):

    return invoice_data