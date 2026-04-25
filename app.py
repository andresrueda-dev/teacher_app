import streamlit as st

st.write(type(st.secrets.get("firebase")))
st.write(st.secrets.get("firebase"))

# ---------------- FIREBASE INIT ----------------
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"])
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------- SECURITY ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- AUTH ----------------
def register_user(email, password):
    user_ref = db.collection("users").document(email)

    if user_ref.get().exists:
        return False, "User already exists"

    user_ref.set({
        "email": email,
        "password": hash_password(password)
    })

    return True, "Account created"


def login_user(email, password):
    user_ref = db.collection("users").document(email)
    user = user_ref.get()

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

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state["user"] = None

# ---------------- LOGOUT ----------------
if st.sidebar.button("Cerrar sesión"):
    st.session_state["user"] = None
    st.rerun()

# ---------------- MENU ----------------
menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

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
    st.sidebar.success(f"👤 {st.session_state['user']}")
    st.title("📊 Classroom Panel")

    tab1, tab2, tab3 = st.tabs(["Students", "Points", "Strategy"])

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
            st.info("No students available")

    # -------- STRATEGY --------
    with tab3:
        st.subheader("Class insights")

        students = get_students(st.session_state["user"])

        if students:
            best = max(students, key=lambda x: x["points"])
            worst = min(students, key=lambda x: x["points"])

            st.success(f"🏆 Top: {best['name']} ({best['points']})")
            st.warning(f"⚠ Needs attention: {worst['name']} ({worst['points']})")
        else:
            st.info("Add students to see insights")
