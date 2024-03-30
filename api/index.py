from fastapi import FastAPI, HTTPException
from firebase_admin import db,credentials
import firebase_admin
import os

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

@app.post("/api/pay")
def pay():
    # Example data to push
    data = {
        "name": "Mortimer 'Morty' Smith"
    }
    
    try:
        # Push data to 'users' node in the Firebase database
        results = db.child("users").push(data)
        # Return the results along with a success message
        return {"success": True, "data": results}
    except Exception as e:
        # Catch and return any errors that occur during the database push
        raise HTTPException(status_code=500, detail=str(e))