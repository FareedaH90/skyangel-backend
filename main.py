
from fastapi import FastAPI, Body, Response
from fastapi.middleware.cors import CORSMiddleware
import os, json, base64
import firebase_admin
from firebase_admin import credentials, firestore

# Decode Firebase credentials from base64 environment variable
firebase_creds = json.loads(
    base64.b64decode(os.environ["FIREBASE_CREDS_B64"]).decode()
)
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Enable CORS for all origins (for development — lock down in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.head("/")
def healthcheck():
    return Response(status_code=200)

@app.get("/")
def root():
    return {"message": "SkyAngel backend is live and ready!"}

@app.post("/get_seat")
def get_seat(payload: dict = Body(...)):
    raw_pnr = payload.get("pnr", "")
    pnr = "".join(raw_pnr.split()).upper()
    print(f"🕵️ Trying to retrieve passenger with PNR: {pnr}")

    doc = db.collection("passengers").document(pnr).get()
    if doc.exists:
        return {
            "status": "success",
            "passenger": doc.to_dict()
        }
    return {
        "status": "error",
        "message": "PNR not found"
    }

@app.post("/assign_seat")
def assign_seat(payload: dict = Body(...)):
    raw_pnr = payload.get("pnr", "")
    seat = payload.get("seat", "")
    pnr = "".join(raw_pnr.split()).upper()
    print(f"✈️ Assigning seat {seat} to PNR: {pnr}")

    db.collection("passengers").document(pnr).update({"seat": seat})
    return {
        "status": "success",
        "pnr": pnr,
        "seat": seat
    }

@app.post("/assign_meal")
def assign_meal(payload: dict = Body(...)):
    raw_pnr = payload.get("pnr", "")
    meal_type = payload.get("meal_type", "")
    pnr = "".join(raw_pnr.split()).upper()
    print(f"🥗 Assigning meal {meal_type} to PNR: {pnr}")

    db.collection("meals").document(f"{pnr}_{meal_type}").set({
        "pnr": pnr,
        "meal_type": meal_type
    })
    return {
        "status": "success",
        "pnr": pnr,
        "meal_type": meal_type
    }

@app.post("/log_transcript")
def log_transcript(payload: dict = Body(...)):
    raw_pnr    = payload.get("pnr", "")
    user_input = payload.get("user_input", "")
    response   = payload.get("response", "")
    pnr = "".join(raw_pnr.split()).upper()
    print(f"📝 Logging transcript for PNR: {pnr}")

    db.collection("transcripts").add({
        "pnr": pnr,
        "user_input": user_input,
        "response": response,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return {"status": "success"}

@app.post("/seed_data")
def seed_data():
    data = [
        # Alice Tan - SQ101
        {"path": "flights/SQ101", "data": {
            "flight_id": "SQ101", "pnr": "PNR001",
            "departure_city": "Singapore", "arrival_city": "Kuala Lumpur",
            "departure_time": "2025-05-22T08:00:00", "gate": "A1",
            "boarding_time": "07:30 AM", "status": "Scheduled"
        }},
        {"path": "passengers/PNR001", "data": {
            "pnr": "PNR001", "name": "Alice Tan",
            "passport_number": "E1234567", "contact_number": "+65 8123 4567",
            "flight_id": "SQ101"
        }},
        {"path": "seats/SQ101_12A", "data": {
            "flight_id": "SQ101", "seat_number": "12A",
            "seat_type": "window", "seat_zone": "front", "is_available": 1
        }},
        {"path": "meals/SQ101_veg", "data": {
            "flight_id": "SQ101", "meal_type": "veg", "availability_count": 5
        }},

        # Rahul Sharma - TR202
        {"path": "flights/TR202", "data": {
            "flight_id": "TR202", "pnr": "PNR002",
            "departure_city": "Singapore", "arrival_city": "Jakarta",
            "departure_time": "2025-05-22T09:30:00", "gate": "B3",
            "boarding_time": "09:00 AM", "status": "Scheduled"
        }},
        {"path": "passengers/PNR002", "data": {
            "pnr": "PNR002", "name": "Rahul Sharma",
            "passport_number": "N9876543", "contact_number": "+65 9654 3210",
            "flight_id": "TR202"
        }},
        {"path": "seats/TR202_15C", "data": {
            "flight_id": "TR202", "seat_number": "15C",
            "seat_type": "aisle", "seat_zone": "middle", "is_available": 0
        }},
        {"path": "meals/TR202_gluten-free", "data": {
            "flight_id": "TR202", "meal_type": "gluten-free", "availability_count": 2
        }},

        # Nguyen Thi Mai - MH303
        {"path": "flights/MH303", "data": {
            "flight_id": "MH303", "pnr": "PNR003",
            "departure_city": "Singapore", "arrival_city": "Bangkok",
            "departure_time": "2025-05-22T10:15:00", "gate": "C5",
            "boarding_time": "09:45 AM", "status": "Scheduled"
        }},
        {"path": "passengers/PNR003", "data": {
            "pnr": "PNR003", "name": "Nguyen Thi Mai",
            "passport_number": "B5432198", "contact_number": "+65 8787 4567",
            "flight_id": "MH303"
        }},
        {"path": "seats/MH303_22B", "data": {
            "flight_id": "MH303", "seat_number": "22B",
            "seat_type": "middle", "seat_zone": "back", "is_available": 1
        }},
        {"path": "meals/MH303_non-veg", "data": {
            "flight_id": "MH303", "meal_type": "non-veg", "availability_count": 4
        }},

        # John Reyes - VN404
        {"path": "flights/VN404", "data": {
            "flight_id": "VN404", "pnr": "PNR004",
            "departure_city": "Singapore", "arrival_city": "Ho Chi Minh City",
            "departure_time": "2025-05-22T11:00:00", "gate": "D2",
            "boarding_time": "10:30 AM", "status": "Delayed"
        }},
        {"path": "passengers/PNR004", "data": {
            "pnr": "PNR004", "name": "John Reyes",
            "passport_number": "P7654321", "contact_number": "+65 9345 2221",
            "flight_id": "VN404"
        }},
        {"path": "seats/VN404_10F", "data": {
            "flight_id": "VN404", "seat_number": "10F",
            "seat_type": "window", "seat_zone": "front", "is_available": 0
        }},
        {"path": "meals/VN404_veg", "data": {
            "flight_id": "VN404", "meal_type": "veg", "availability_count": 3
        }},

        # Siti Aisyah - PR505
        {"path": "flights/PR505", "data": {
            "flight_id": "PR505", "pnr": "PNR005",
            "departure_city": "Singapore", "arrival_city": "Manila",
            "departure_time": "2025-05-22T12:00:00", "gate": "E1",
            "boarding_time": "11:30 AM", "status": "Scheduled"
        }},
        {"path": "passengers/PNR005", "data": {
            "pnr": "PNR005", "name": "Siti Aisyah",
            "passport_number": "L1111222", "contact_number": "+65 8111 9999",
            "flight_id": "PR505"
        }},
        {"path": "seats/PR505_18D", "data": {
            "flight_id": "PR505", "seat_number": "18D",
            "seat_type": "aisle", "seat_zone": "middle", "is_available": 1
        }},
        {"path": "meals/PR505_veg", "data": {
            "flight_id": "PR505", "meal_type": "veg", "availability_count": 6
        }},
    ]

    for doc in data:
        collection, doc_id = doc["path"].split("/")
        db.collection(collection).document(doc_id).set(doc["data"])

    return {"status": " Seed data uploaded successfully"}
    for doc in data:
        collection, doc_id = doc["path"].split("/")
        db.collection(collection).document(doc_id).set(doc["data"])
    return {"status": " Seed data uploaded successfully"}

