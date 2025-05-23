
import os, json, base64
from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, firestore
from fastapi.middleware.cors import CORSMiddleware


# Decode base64 and parse the credentials
firebase_creds = json.loads(base64.b64decode(os.environ["FIREBASE_CREDS_B64"]).decode())
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_seat")
def get_seat(pnr: str):
    passenger_docs = db.collection("passengers").where("pnr", "==", pnr).stream()
    for doc in passenger_docs:
        passenger = doc.to_dict()
        flight_id = passenger.get("flight_id")
        seat_docs = db.collection("seats")             .where("flight_id", "==", flight_id)             .where("is_available", "==", 1).limit(1).stream()
        for seat in seat_docs:
            return seat.to_dict()
    return {"error": "PNR not found or no seat available"}
