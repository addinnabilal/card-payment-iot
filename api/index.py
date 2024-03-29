from fastapi import FastAPI
import pyrebase
import os

firebaseConfig = {
  'apiKey': os.environ.get('API_KEY'),
  'authDomain': os.environ.get('AUTH_DOMAIN'),
  'databaseURL': os.environ.get('DATABASE_URL'),
  'projectId': os.environ.get('PROJECT_ID'),
  'storageBucket': os.environ.get('STORAGE_BUCKET'),
  'messagingSenderId': os.environ.get('MESSAGING_SENDER_ID'),
  'appId': os.environ.get('APP_ID'),
  'measurementId': os.environ.get('MEASUREMENT_ID')
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

app = FastAPI()

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.post("/api/pay")
def pay():
    # get the current balance, display to ui, and return if success
    data = {
    "name": "Mortimer 'Morty' Smith"
    }

    # Pass the user's idToken to the push method
    db.child("users").push(data)
