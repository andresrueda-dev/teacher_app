import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json

if not firebase_admin._apps:
    firebase_dict = json.loads(st.secrets["firebase_json"])
    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()
