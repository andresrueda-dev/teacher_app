import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
import pandas as pd
from datetime import datetime
import streamlit as st

if "students" not in st.session_state:
    st.session_state.students = []

st.subheader("➕ Add Students")

new_student = st.text_input("Student name")

if st.button("Add student"):
    if new_student:
        st.session_state.students.append({"name": new_student, "points": 0})
        st.success(f"{new_student} added!")

st.subheader("📋 Student List")

for student in st.session_state.students:
    st.write(f"{student['name']} - {student['points']} pts")

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Teacher App", layout="wide")

st.markdown("""
<style>
button {
    height: 60px;
    font-size: 18px !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FIREBASE ----------------
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- SECURITY ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- AUTH ----------------
def register_user(email, password):
    ref = db.collection("users").document(email)

    if ref.get().exists:
        return False, "User already exists"

    ref.set({
        "email": email,
        "password": hash_password(password)
    })

    return True, "Account created"

def login_user(email, password):
    ref = db.collection("users").document(email)
    user = ref.get()

    if not user.exists:
        return False, "User not found"

    data = user.to_dict()

    if data["password"] == hash_password(password):
        return True, "Login successful"
    else:
        return False, "Incorrect password"

# ---------------- GROUPS ----------------
def create_group(user, name, grade):
    db.collection("groups").add({
        "user": user,
        "name": name,
        "grade": grade
    })

def get_groups(user):
    docs = db.collection("groups").where("user", "==", user).stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

# ---------------- STUDENTS ----------------
def add_student(user, name, group_id):
    db.collection("students").add({
        "user": user,
        "name": name,
        "group_id": group_id,
        "points": 0
    })

def get_students(user, group_id=None):
    query = db.collection("students").where("user", "==", user)

    if group_id:
        query = query.where("group_id", "==", group_id)

    docs = query.stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in docs]

# ---------------- LISTA PREDEFINIDA ----------------
def load_my_students(user, group_id):
    students_list = [
        "Andrea López","Luis Martínez","Carlos Ramírez",
        "Sofía Hernández","Valeria Torres","Diego Castro",
        "Fernanda Ruiz","Jorge Mendoza","Camila Ortiz","Daniel Pérez"
    ]

    docs = db.collection("students").where("group_id", "==", group_id).stream()
    for doc in docs:
        db.collection("students").document(doc.id).delete()

    for name in students_list:
        db.collection("students").add({
            "user": user,
            "group_id": group_id,
            "name": name,
            "points": 0
        })

# ---------------- POINTS + LOG ----------------
def add_points(student_id, points, user, behavior):
    db.collection("students").document(student_id).update({
        "points": firestore.Increment(points)
    })

    db.collection("logs").add({
        "student_id": student_id,
        "points": points,
        "behavior": behavior,
        "user": user,
        "timestamp": datetime.now()
    })

def get_logs(user):
    docs = db.collection("logs").where("user", "==", user).stream()
    return [doc.to_dict() for doc in docs]

# ---------------- IA (RIESGO) ----------------
def risk_analysis(student_id, logs):
    records = [l for l in logs if l["student_id"] == student_id]

    if len(records) < 3:
        return "🟡"

    last = records[-5:]
    neg = sum(1 for r in last if r["points"] < 0)

    if neg >= 3:
        return "🔴"
    elif neg == 2:
        return "🟡"
    return "🟢"

# ---------------- UI ----------------
st.sidebar.title("📱 Teacher App")

if st.session_state.user:
    st.sidebar.success(st.session_state.user)
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.user = None
        st.rerun()

menu = st.sidebar.radio(
    "Menu",
    ["Login","Register"] if not st.session_state.user else
    ["🏠 Home","🎯 Points","📊 Ranking","🚨 Alerts"]
)

# ---------------- LOGIN ----------------
if not st.session_state.user:

    if menu == "Login":
        st.title("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            ok, msg = login_user(email, password)
            if ok:
                st.session_state.user = email
                st.rerun()
            else:
                st.error(msg)

    if menu == "Register":
        st.title("Register")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            ok, msg = register_user(email, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

# ---------------- APP ----------------
else:

    groups = get_groups(st.session_state.user)

    # SI NO HAY GRUPOS → CREAR AUTOMÁTICO
    if not groups:
        create_group(st.session_state.user, "Grupo 1", "1")
        groups = get_groups(st.session_state.user)

    group_id = groups[0]["id"]

    # SI NO HAY ALUMNOS → CARGAR
    students = get_students(st.session_state.user, group_id)

    if not students:
        load_my_students(st.session_state.user, group_id)
        students = get_students(st.session_state.user, group_id)

    # ---------------- HOME ----------------
    if menu == "🏠 Home":
        st.title("📱 Teacher App")

        top = sorted(students, key=lambda x: x["points"], reverse=True)[:3]

        st.subheader("🏆 Top Students")
        for t in top:
            st.success(f"{t['name']} - {t['points']} pts")

    # ---------------- POINTS ----------------
    if menu == "🎯 Points":

        behaviors = {
            "👍": 2,
            "📚": 2,
            "🤝": 3,
            "⏰": -1,
            "❌": -2
        }

        for s in students:
            st.subheader(f"{s['name']} ({s['points']})")

            cols = st.columns(len(behaviors))

            for i, (b, val) in enumerate(behaviors.items()):
                if cols[i].button(b, key=f"{s['id']}_{b}"):
                    add_points(s["id"], val, st.session_state.user, b)
                    st.rerun()

    # ---------------- RANKING ----------------
    if menu == "📊 Ranking":
        st.title("Ranking")

        df = pd.DataFrame(students).sort_values("points", ascending=False)
        st.dataframe(df[["name","points"]])

    # ---------------- ALERTS ----------------
    if menu == "🚨 Alerts":
        st.title("Alerts")

        logs = get_logs(st.session_state.user)

        for s in students:
            risk = risk_analysis(s["id"], logs)

            if risk == "🔴":
                st.error(f"{s['name']} en riesgo")
            elif risk == "🟡":
                st.warning(f"{s['name']} atención")
            else:
                st.success(f"{s['name']} bien")
