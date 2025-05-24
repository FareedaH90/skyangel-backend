
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
    # (Example seed data — remove or secure this endpoint in production)
    data = [
        # ... your seed entries here, as in your existing list ...
    ]
    for doc in data:
        collection, doc_id = doc["path"].split("/")
        db.collection(collection).document(doc_id).set(doc["data"])
    return {"status": " Seed data uploaded successfully"}

