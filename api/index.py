from fastapi import FastAPI, HTTPException
from firebase_admin import db,credentials
import firebase_admin
import os
from pydantic import BaseModel

from datetime import date


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

@app.post("/api/pay")
def pay(payment_request: PaymentRequest):
    client_id = payment_request.client_id
    amount = payment_request.amount

    # get client data from firebase. if not found, add client data
    ref = db.reference('clients')
    client = ref.child(client_id).get()
    if client is None:
        ref.child(client_id).set({
            'balance': initial_balance,
            'transactions': [
                {  
                    'date': date,
                    'amount': amount,
                    'type': 'credit'
                }
            ]
        })
    else:
        ref.child(client_id).update({
            'balance': client['balance'] - amount
        })
        ref.child(client_id).child('transactions').push({
            'date': date,
            'amount': amount,
            'type': 'credit'
        })
    
    