import streamlit as st
from firebase_config import login_user, add_student, get_students, add_points, db

st.set_page_config(page_title="Teacher Pro System")

st.title("🎓 Teacher Control System")

# 🔥 BOTÓN LOGOUT
if st.sidebar.button("Cerrar sesión"):
    st.session_state.clear()
    st.rerun()

# 🔍 DEBUG (puedes borrarlo después)
st.sidebar.write("DEBUG USER:", st.session_state.get("user"))

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

# -------- SI NO HAY USUARIO → LOGIN/REGISTER --------
if "user" not in st.session_state:

    # -------- LOGIN --------
    if menu == "Login":
        st.subheader("Login")

        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if login_email and login_password:
                ok, msg = login_user(login_email, login_password)

                if ok:
                    st.session_state["user"] = login_email
                    st.success("Welcome 🔥")
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Fill all fields")

    # -------- REGISTER --------
    if menu == "Register":
        st.subheader("Create Account")

        reg_email = st.text_input("New email", key="reg_email")
        reg_password = st.text_input("New password", type="password", key="reg_pass")

        if st.button("Create account"):
            if not reg_email or not reg_password:
                st.warning("Fill all fields")
            else:
                try:
                    ref = db.collection("users").document(reg_email)

                    ref.set({
                        "email": reg_email,
                        "password": reg_password
                    })

                    st.success("✅ Account created")
                    st.session_state["user"] = reg_email
                    st.rerun()

                except Exception as e:
                    st.error(str(e))


# -------- SI HAY USUARIO → DASHBOARD --------
else:

    st.sidebar.success(f"👤 {st.session_state['user']}")

    st.title("📊 Classroom Panel")

    tab1, tab2, tab3 = st.tabs(["Students", "Points", "Strategy"])

    # -------- STUDENTS --------
    with tab1:
        name = st.text_input("Student name", key="student_name")

        if st.button("Add student"):
            if name:
                add_student(st.session_state["user"], name)
                st.success("Student added")
            else:
                st.warning("Enter a name")

        students = get_students(st.session_state["user"])

        for s in students:
            st.write(f"👤 {s['name']} ⭐ {s['points']}")

    # -------- POINTS --------
    with tab2:
        students = get_students(st.session_state["user"])

        for s in students:
            col1, col2, col3 = st.columns([3, 1, 1])

            col1.write(f"{s['name']} ({s['points']})")

            if col2.button(f"+1 {s['id']}"):
                add_points(s["id"], 1)

            if col3.button(f"-1 {s['id']}"):
                add_points(s["id"], -1)

    # -------- STRATEGY --------
    with tab3:
        students = get_students(st.session_state["user"])

        if students:
            best = max(students, key=lambda x: x["points"])
            worst = min(students, key=lambda x: x["points"])

            st.success(f"Top: {best['name']} ⭐ {best['points']}")
            st.warning(f"Attention: {worst['name']} ⚠ {worst['points']}")
        else:
            st.info("No students yet")
