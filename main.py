
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, json, base64
import firebase_admin
from firebase_admin import credentials, firestore

# Decode Firebase credentials from base64 environment variable
firebase_creds = json.loads(base64.b64decode(os.environ["FIREBASE_CREDS_B64"]).decode())
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Enable CORS for all origins (optional, adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for sanity check
@app.get("/")
def root():
    return {"message": "SkyAngel backend is live and ready!"}

# Get seat info by PNR
@app.get("/get_seat")
def get_seat(pnr: str):
    doc = db.collection("passengers").document(pnr).get()
    return doc.to_dict() if doc.exists else {"error": "PNR not found"}

# Assign seat to passenger
@app.post("/assign_seat")
def assign_seat(pnr: str, seat: str):
    db.collection("passengers").document(pnr).update({"seat": seat})
    return {"status": "Seat updated", "pnr": pnr, "seat": seat}

# Assign meal to passenger
@app.post("/assign_meal")
def assign_meal(pnr: str, meal_type: str):
    doc_ref = db.collection("meals").document(f"{pnr}_{meal_type}")
    doc_ref.set({
        "pnr": pnr,
        "meal_type": meal_type
    })
    return {"status": "Meal assigned", "pnr": pnr, "meal_type": meal_type}

# Log user-agent conversation transcript
@app.post("/log_transcript")
def log_transcript(pnr: str, user_input: str, response: str):
    db.collection("transcripts").add({
        "pnr": pnr,
        "user_input": user_input,
        "response": response,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return {"status": "Transcript logged"}
