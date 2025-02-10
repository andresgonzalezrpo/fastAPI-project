from models import Customer, Transaction, TransactionCreate
from fastapi import APIRouter, HTTPException, Query,status
from sqlmodel import select
from db import SessionDep

router = APIRouter()

@router.post('/transactions',status_code=status.HTTP_201_CREATED, tags = ['transactions']) # esta en mayuscula por que es una recomendacion cuando se crea una API rest
async def create_transaction(transaction_data: TransactionCreate, session: SessionDep):
    #Podemos usar la sesion para verificar que el customerid si exista
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get('customer_id'))
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist")
    #Si existe ya podemos crear la transaction

    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return transaction_db

@router.get("/transactions", tags = ['transactions'])
async def list_transaction(session: SessionDep, skip: int = Query(0, description="Registros a omitir"),
                           limit: int = Query(10, description="Número de registros")):
    query = select(Transaction).offset(skip).limit(limit)
    transactions = session.exec(query).all()
    return transactions


