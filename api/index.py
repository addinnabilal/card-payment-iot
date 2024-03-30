from fastapi import FastAPI, HTTPException
from firebase_admin import db,credentials
import firebase_admin
import os
from pydantic import BaseModel

import datetime


# Firebase configuration from environment variables
firebaseConfig = {
'type': 'service_account',
'project_id': os.getenv("FIREBASE_PROJECT_ID"),
'private_key_id': os.getenv("FIREBASE_KEY_ID"),
'private_key': os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
'client_email': os.getenv("FIREBASE_CLIENT_EMAIL"),
'client_id': os.getenv("FIREBASE_CLIENT_ID"),
'auth_uri': os.getenv("FIREBASE_AUTH_URI"),
'token_uri': os.getenv("FIREBASE_TOKEN_URI"),
'auth_provider_x509_cert_url': os.getenv("FIREBASE_AUTH_PROVIDER"),
'client_x509_cert_url': os.getenv("FIREBASE_CLIENT_CERT"),
'universe_domain': "googleapis.com"
}



cred = credentials.Certificate(firebaseConfig)
firebase_admin.initialize_app(cred,{
    'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
})

app = FastAPI()

@app.get("/api/test")
def test_api():
    return {"message": "Hello World"}

class PaymentRequest(BaseModel):
    client_id: str
    amount: float

@app.get("/api/last_transaction")
def get_last_transaction():
    ref = db.reference('/last_transaction')
    last_transaction = ref.get()
    return last_transaction

@app.get("/api/transactions/{client_id}")
def get_transactions(client_id: str):
    ref = db.reference('clients')
    client = ref.child(client_id).get()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    transactions = client['transactions']
    {
        "remaining_balance": client['balance'],
        "transactions": transactions
    }
    return transactions

@app.post("/api/pay")
def pay(payment_request: PaymentRequest):
    client_id = payment_request.client_id
    amount = payment_request.amount
    initial_balance = 145000   

    # Format the date for the transaction
    date = datetime.date.today().strftime("%Y-%m-%d")

    # Get client data from Firebase. If not found, add client data.
    ref = db.reference('clients')
    ref_latest = db.reference('/latest_transaction')
    client = ref.child(client_id).get()

    transaction = {
        'date': date,
        'amount': amount,
        'type': 'credit'
    }

    if client is None:
        ref.child(client_id).set({
            'balance': initial_balance - amount,  # Assuming the first transaction is also deducted
            'transactions': [
                transaction
            ]
        })
        # store in the last transaction
        if ref_latest.get() is None:
            ref_latest.set({
                'client_id': client_id,
                'balance': client['balance'] ,
                'last_transaction': transaction
            })
        else:
            ref_latest.update({
                'client_id': client_id,
                 'balance': client['balance'] ,
                'last_transaction': transaction
            })
    else:
        new_balance = client['balance'] - amount
        if new_balance < 0:
            # Handle insufficient funds
            raise HTTPException(status_code=400, detail="Insufficient funds")
        ref.child(client_id).update({
            'balance': new_balance
        })
        # Assuming transactions is a list. If it's meant to be a collection of objects, consider a push operation instead.
        transactions_ref = ref.child(client_id).child('transactions').push()
        transactions_ref.set(transaction)
        if ref_latest.get() is None:
            ref_latest.set({
                'client_id': client_id,
                'balance': client['balance'] ,
                'last_transaction': transaction
            })
        else:
            ref_latest.update({
                'client_id': client_id,
                'balance': client['balance'] ,
                'last_transaction': transaction
            })
    return {"message": "Transaction processed successfully."}
    