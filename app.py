import streamlit as st
from firebase_config import register_user, login_user, add_student, get_students, add_points, db

st.set_page_config(page_title="Teacher Pro System")

st.title("🎓 Teacher Control System")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# -------- LOGIN --------
if menu == "Login":
    st.subheader("Login")

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

# -------- REGISTER --------
elif menu == "Register":
    st.subheader("Create Account")

    email = st.text_input("New email")
    password = st.text_input("New password", type="password")

    if st.button("Create account"):
        st.write("🔍 intentando guardar...")

        if not email or not password:
            st.warning("Campos vacíos")
        else:
            try:
                ref = db.collection("users").document(email)

                st.write("1. referencia creada")

                # 🔥 GUARDADO DIRECTO (SIN VALIDACIÓN)
                ref.set({
                    "email": email,
                    "password": password
                })

                st.success("✅ GUARDADO REAL")
                st.write("2. documento creado")

                st.session_state["user"] = email
                st.rerun()

            except Exception as e:
                st.error("ERROR REAL:")
                st.write(e)
# -------- DASHBOARD --------
if "user" in st.session_state:

    st.sidebar.success(f"👤 {st.session_state['user']}")

    st.title("📊 Classroom Panel")

    tab1, tab2, tab3 = st.tabs(["Students", "Points", "Strategy"])

    # -------- STUDENTS --------
    with tab1:
        name = st.text_input("Student name")

        if st.button("Add student"):
            add_student(st.session_state["user"], name)
            st.success("Added")

        students = get_students(st.session_state["user"])

        for s in students:
            st.write(f"{s['name']} ⭐ {s['points']}")

    # -------- POINTS --------
    with tab2:
        students = get_students(st.session_state["user"])

        for s in students:
            col1, col2, col3 = st.columns([3, 1, 1])

            col1.write(f"{s['name']} ({s['points']})")

            if col2.button(f"+ {s['id']}"):
                add_points(s["id"], 1)

            if col3.button(f"- {s['id']}"):
                add_points(s["id"], -1)

    # -------- STRATEGY --------
    with tab3:
        students = get_students(st.session_state["user"])

        if students:
            best = max(students, key=lambda x: x["points"])
            worst = min(students, key=lambda x: x["points"])

            st.success(f"Top: {best['name']} ⭐ {best['points']}")
            st.warning(f"Attention: {worst['name']} ⚠ {worst['points']}")
