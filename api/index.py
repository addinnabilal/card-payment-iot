from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, db
import os

# Firebase configuration from environment variables
firebaseConfig = {
  "type": "service_account",
  "project_id": "card-payment-iot",
  "private_key_id": "3609ecc3a6bf6be0f54e08abfaa8649cf5e2185b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtjzkowOARZOWS\nA0Ie0fr5+WV2s0gnyu568TXU9JHC4U5wazTmRDpmdAMurkUMXr6Sg1NB0kSydh+C\nStRpjekwMqEupPKol6zEpI0r0BSjH6l7Ak5M7FOjWPkXly2P0TPu2WNMfX66/75g\n/OxY7AhpBe9T3xvvOG7BTEeAYKdAFsriPZjfXu5u1J/tNtmvBCjouFwPr9mCwk66\nTlbiBHejyraejOg3OW3skWYj5Cet1/34wLWbL+Uyu3tUylFoKasFsQIUvw4XE4ZR\nGMnQ5xyucT9tdpPSgEoH0LYDp4u00rKLU66H08SjSgj++m7znbo2sVweEngTyCYJ\nH4pZXQKvAgMBAAECggEAC8kEw8XWZpKi3MItjGPhdnWfFFXX3vfdL2pPUk6/J8Fe\nhFdgnV2MV6ZQtwFCErUg8gL1NYF+hQhssE9o0rgTrwr+aJPudFCZpzVYmV0voY9b\nVffR8vroh62EJebFQxWcwKnF9TeKUk6zvJNAG0j/yIiMzUsCSGwHvUbIONPsrMx3\n8q/2J9CmQ80Y0Z3E0r/2a5PdH93kVDQzUXqxB59T+kFswYooQbauBG1EmjDa9bOD\ndwgwShOGwlzzaUOi5aSyjfbEJwVyq0fte7argMi3BjRDHVhqhSJdSucwYNODo1Ny\nkLwx63RVtXS6ruhqEFgGqvPZlXpV/QxqtOpO0esH1QKBgQDrQdfxhBCwyog+yxQi\niZ+gaTusrjJWv0WqsGGVFHkfV8gCyO6jtmB1RGmak7oEhTcHKNxOIWnmBWfAAAOU\n7hJP/YVkHk5437QDf6DaLtp2/CPIoZGGxpRoQ5rjgQtvunVCCzE2A9Oa0bW9vRK0\nYGpNaUnp2fAlwR8nyeS1z2vk3QKBgQC83MGvYoHxQoCsVhOUedzZNtM2LfmQVZAN\n8+4gp5rEBN29zE3US/wgJGx/poQPlkjJVdA2mgvmd2iMyjZ4mXJvwErduSPe5NPQ\nMSxajC/ErcodLx2Y3EcES54mCXdkAARMt+3uW8Z+abq2mj/0v2URuIpS+2DCIZYc\nJqVucjE2+wKBgQDNvT1+x8JY+iaA09T+B2GERcOcVpNLbecdSTdtywPKN1iBpvuc\nTMi6hWPdfUf24BGpv0A7S9lzAlMjhF+dhT6amdpoHmD+MJUbYihn5wXDfOpGcZX1\nSgFL1aPFRnub8HLPmT4mQN5zzOal0o5jFNaicGvliWUNf4EhqNzNa2KuOQKBgQCL\n1PsGqu3AvldcwcJvfSa6ILCS/ck4R1GIMyINRWr+VQgEfd7mH3hGKBG5FYXTsJal\nkwa9VqMW+TQMga+A7UPgX8ROk8RuRIhbLf1D8WVwvqfVocvNINLn6EDosruV67lD\nQC9G+uZlNE0M4/oUcR0Y2MR5mitSsOFeaHK16pBrvwKBgFKvz8JYLTLcKKW7dcod\nva8jBLGL8t76aLxf2z6qnt9wbBnV1DNSAa0HEO+29Q4MCX9gY/kXrA6IBO33P/wE\nFyiCDxbgeuFULmXgYwi6OLjvN7AoKXeWRLxOLlsp48BUOZFDD7Uhboq+hH9fRcvy\nNcKY2zdU7WQTpnDY4MiAyFvI\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-vz0ax@card-payment-iot.iam.gserviceaccount.com",
  "client_id": "110689304538656209533",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-vz0ax%40card-payment-iot.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
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