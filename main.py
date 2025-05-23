
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore
import json

firebase_creds = json.loads(os.environ["FIREBASE_CREDS"])
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)

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
