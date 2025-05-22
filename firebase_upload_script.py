
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase-creds.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Example data to upload
data = [
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
    }}
]

for doc in data:
    path_parts = doc["path"].split("/")
    if len(path_parts) == 2:
        collection, doc_id = path_parts
        db.collection(collection).document(doc_id).set(doc["data"])
        print(f"Uploaded to {doc['path']}")
