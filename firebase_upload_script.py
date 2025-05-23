import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Decode the base64 FIREBASE_CREDS env var and write to file
firebase_creds_base64 = os.environ["FIREBASE_CREDS"]
firebase_creds_json = json.loads(firebase_creds_base64)
with open("firebase-creds.json", "w") as f:
    json.dump(firebase_creds_json, f)

# Initialize Firebase
cred = credentials.Certificate("firebase-creds.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Batch upload: 10 passengers

data = [
    # Alice Tan
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

    # Rahul Sharma
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

    # Nguyen Thi Mai
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

    # John Reyes
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

    # Siti Aisyah
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
    }}
]


for doc in data:
    path_parts = doc["path"].split("/")
    if len(path_parts) == 2:
        collection, doc_id = path_parts
        db.collection(collection).document(doc_id).set(doc["data"])
        print(f"Uploaded to {doc['path']}")
