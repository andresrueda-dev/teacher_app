import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
import pandas as pd

# ---------------- FIREBASE INIT ----------------
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)

db = firestore.client()

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

# ---------------- STUDENTS ----------------
def add_student(user, name):
    db.collection("students").add({
        "user": user,
        "name": name,
        "points": 0
    })


def get_students(user):
    docs = db.collection("students").where("user", "==", user).stream()
    
    students = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        students.append(data)
    
    return students


def add_points(student_id, points):
    db.collection("students").document(student_id).update({
        "points": firestore.Increment(points)
    })

# ---------------- DEMO DATA ----------------
def load_demo_data(user):
    demo_students = [
        {"name": "Ana", "points": 12},
        {"name": "Luis", "points": 5},
        {"name": "Carlos", "points": -2},
        {"name": "María", "points": 18},
        {"name": "Sofía", "points": 9},
        {"name": "Diego", "points": 0},
        {"name": "Valeria", "points": 15},
        {"name": "Jorge", "points": 3}
    ]

    docs = db.collection("students").where("user", "==", user).stream()
    for doc in docs:
        db.collection("students").document(doc.id).delete()

    for s in demo_students:
        db.collection("students").add({
            "user": user,
            "name": s["name"],
            "points": s["points"]
        })

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# ---------------- SIDEBAR ----------------
st.sidebar.title("Menu")

if st.session_state["user"]:
    st.sidebar.success(f"👤 {st.session_state['user']}")

    if st.sidebar.button("Cerrar sesión"):
        st.session_state["user"] = None
        st.rerun()

    st.sidebar.markdown("### 🧪 Demo")
    if st.sidebar.button("Cargar datos demo"):
        load_demo_data(st.session_state["user"])
        st.success("Datos demo cargados 🚀")
        st.rerun()

menu = st.sidebar.selectbox("Navigation", ["Login", "Register"])

# =========================================================
# ---------------- SIN USUARIO ----------------
# =========================================================
if not st.session_state["user"]:

    if menu == "Login":
        st.title("🔐 Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email and password:
                ok, msg = login_user(email, password)

                if ok:
                    st.session_state["user"] = email
                    st.success("Welcome 🔥")
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Fill all fields")

    elif menu == "Register":
        st.title("🆕 Create Account")

        email = st.text_input("New email")
        password = st.text_input("New password", type="password")

        if st.button("Create account"):
            if email and password:
                ok, msg = register_user(email, password)

                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Fill all fields")

# =========================================================
# ---------------- CON USUARIO ----------------
# =========================================================
else:
    st.title("📊 Classroom Panel")

    tab1, tab2, tab3 = st.tabs(["Students", "Points", "Dashboard"])

    # -------- STUDENTS --------
    with tab1:
        st.subheader("Add student")

        name = st.text_input("Student name")

        if st.button("Add student"):
            if name:
                add_student(st.session_state["user"], name)
                st.success("Student added")
                st.rerun()
            else:
                st.warning("Enter a name")

        st.divider()

        students = get_students(st.session_state["user"])

        if students:
            for s in students:
                st.write(f"👤 {s['name']} ⭐ {s['points']}")
        else:
            st.info("No students yet")

    # -------- POINTS --------
    with tab2:
        st.subheader("Manage points")

        students = get_students(st.session_state["user"])

        if students:
            for s in students:
                col1, col2, col3 = st.columns([3, 1, 1])

                col1.write(f"{s['name']} ({s['points']})")

                if col2.button(f"+1 {s['id']}"):
                    add_points(s["id"], 1)
                    st.rerun()

                if col3.button(f"-1 {s['id']}"):
                    add_points(s["id"], -1)
                    st.rerun()
        else:
            st.info("No students")

    # -------- DASHBOARD --------
    with tab3:
        st.subheader("📊 Class Dashboard")

        students = get_students(st.session_state["user"])

        if students:
            df = pd.DataFrame(students)
            df = df.sort_values(by="points", ascending=False)

            st.markdown("### 🏆 Top Students")
            for _, row in df.head(3).iterrows():
                st.success(f"{row['name']} — {row['points']} pts")

            st.markdown("### ⚠ Students at Risk")
            risk = df[df["points"] <= 0]

            if not risk.empty:
                for _, row in risk.iterrows():
                    st.warning(f"{row['name']} — {row['points']} pts")
            else:
                st.info("No students at risk")

            st.markdown("### 📊 Points Chart")
            chart_df = df[["name", "points"]].set_index("name")
            st.bar_chart(chart_df)

            st.markdown("### 📋 Data Table")
            st.dataframe(df)

        else:
            st.info("Add students first")
