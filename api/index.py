from fastapi import FastAPI, HTTPException
from pyrebase import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyDqaMaVIJxlgV5Ob3cvnpoY2mbOc-hmYpw",
  'authDomain': "card-payment-iot.firebaseapp.com",
  'databaseURL': "https://card-payment-iot-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "card-payment-iot",
  'storageBucket': "card-payment-iot.appspot.com",
  'messagingSenderId': "1044993620317",
  'appId': "1:1044993620317:web:ca1ca81f7e845ba94410b4",
  'measurementId': "G-907NCNNEH5"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

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
        # results = db.child("users").push(data)
        # Return the results along with a success message
        return {"success": True, "data": "test"}
    except Exception as e:
        # Catch and return any errors that occur during the database push
        raise HTTPException(status_code=500, detail=str(e))