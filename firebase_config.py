import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

if not firebase_admin._apps:
firebase_json = '''
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nABC123...\n-----END PRIVATE KEY-----\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "...",
  "token_uri": "...",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
'''

# ---------------- ALUMNOS ----------------

def add_student(teacher, name):
    db.collection("students").add({
        "teacher": teacher,
        "name": name,
        "points": 0
    })


def get_students(teacher):
    docs = db.collection("students").where("teacher", "==", teacher).stream()
    return [doc.to_dict() | {"id": doc.id} for doc in docs]


def add_points(student_id, points):
    ref = db.collection("students").document(student_id)
    student = ref.get().to_dict()

    new_points = student["points"] + points
    ref.update({"points": new_points})
