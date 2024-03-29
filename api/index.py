from fastapi import FastAPI, HTTPException
# from pyrebase import pyrebase
# import os

# # Firebase configuration from environment variables
# firebaseConfig = {
#   'apiKey': os.environ.get('API_KEY'),
#   'authDomain': os.environ.get('AUTH_DOMAIN'),
#   'databaseURL': os.environ.get('DATABASE_URL'),
#   'projectId': os.environ.get('PROJECT_ID'),
#   'storageBucket': os.environ.get('STORAGE_BUCKET'),
#   'messagingSenderId': os.environ.get('MESSAGING_SENDER_ID'),
#   'appId': os.environ.get('APP_ID'),
#   'measurementId': os.environ.get('MEASUREMENT_ID')
# }

# firebase = pyrebase.initialize_app(firebaseConfig)
# auth = firebase.auth()
# db = firebase.database()

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
        return {"success": True, "data": results}
    except Exception as e:
        # Catch and return any errors that occur during the database push
        raise HTTPException(status_code=500, detail=str(e))