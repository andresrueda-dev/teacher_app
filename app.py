import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Teacher SaaS PRO", layout="wide")

SUPABASE_URL = "https://lzyrlveqjuoidlznkslj.supabase.co"
SUPABASE_KEY = "PEGA_AQUI_TU_publishable_key"

# ---------------- LOGIN ----------------
def login(email, password):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"

    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "password": password
    }

    res = requests.post(url, json=data, headers=headers)

    if res.status_code == 200:
        return res.json()
    else:
        return None

# ---------------- AUTH UI ----------------
if "user" not in st.session_state:
    st.title("🔐 Teacher Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login(email, password)

        if user:
            st.session_state.user = user
            st.success("Welcome 🚀")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- MENU ----------------
menu = st.sidebar.radio("Menu", [
    "🏠 Dashboard",
    "🏫 Groups",
    "👥 Students"
])

# ---------------- API FUNCTIONS ----------------
def create_group(name, grade):
    url = f"{SUPABASE_URL}/rest/v1/groups"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {st.session_state.user['access_token']}",
        "Content-Type": "application/json"
    }

    data = {
        "name": name,
        "grade": grade,
        "user_id": st.session_state.user["user"]["id"]
    }

    requests.post(url, json=data, headers=headers)


def get_groups():
    url = f"{SUPABASE_URL}/rest/v1/groups?user_id=eq.{st.session_state.user['user']['id']}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {st.session_state.user['access_token']}"
    }

    res = requests.get(url, headers=headers)
    return res.json()


def add_student(name, group_id):
    url = f"{SUPABASE_URL}/rest/v1/students"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {st.session_state.user['access_token']}",
        "Content-Type": "application/json"
    }

    data = {
        "name": name,
        "group_id": group_id
    }

    requests.post(url, json=data, headers=headers)


def get_students(group_id):
    url = f"{SUPABASE_URL}/rest/v1/students?group_id=eq.{group_id}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {st.session_state.user['access_token']}"
    }

    res = requests.get(url, headers=headers)
    return res.json()

# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":
    st.title("📊 Dashboard")
    st.info("Sistema conectado a la nube 🚀")

# ---------------- GROUPS ----------------
elif menu == "🏫 Groups":
    st.title("🏫 Create Group")

    grade = st.selectbox("Grade", ["1", "2", "3"])
    group_letter = st.text_input("Group (A, B...)")

    if st.button("Create Group"):
        name = f"{grade}{group_letter}"
        create_group(name, grade)
        st.success("Group created ✅")

    st.subheader("Your Groups")

    groups = get_groups()

    for g in groups:
        st.write(f"📚 Grade {g['grade']} - {g['name']}")

# ---------------- STUDENTS ----------------
elif menu == "👥 Students":
    st.title("👥 Students")

    groups = get_groups()

    if not groups:
        st.warning("Create a group first ⚠️")
    else:
        group_names = [g["name"] for g in groups]
        selected_group = st.selectbox("Select group", group_names)

        group_id = [g["id"] for g in groups if g["name"] == selected_group][0]

        student_name = st.text_input("Student name")

        if st.button("Add Student"):
            add_student(student_name, group_id)
            st.success("Saved in cloud 🚀")

        st.subheader("Students List")

        students = get_students(group_id)

        for s in students:
            st.write(f"👤 {s['name']}")
