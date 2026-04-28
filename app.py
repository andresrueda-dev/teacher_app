import streamlit as st
import sqlite3
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Teacher Manager PRO", layout="wide")

# ---------------- DB ----------------
conn = sqlite3.connect("school.db", check_same_thread=False)
c = conn.cursor()

# ---- TABLES ----
c.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    grade TEXT,
    teacher_id INTEGER)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    group_id INTEGER)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT)
""")

conn.commit()

# ---------------- LOGIN ----------------
if "teacher_id" not in st.session_state:
    st.title("🔐 Login Teacher")

    user = st.text_input("User")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT id FROM teachers WHERE username=? AND password=?", (user, pwd))
        result = c.fetchone()

        if result:
            st.session_state.teacher_id = result[0]
            st.success("Welcome!")
            st.rerun()
        else:
            st.error("User not found")

    st.stop()

# ---------------- MENU ----------------
menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Groups",
    "Students",
    "Attendance"
])

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.title("📊 Dashboard")

    c.execute("SELECT COUNT(*) FROM students")
    total_students = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM groups")
    total_groups = c.fetchone()[0]

    st.metric("Students", total_students)
    st.metric("Groups", total_groups)

# ---------------- GROUPS ----------------
elif menu == "Groups":
    st.title("🏫 Groups")

    grade = st.selectbox("Grade", ["1", "2", "3"])
    group_letter = st.text_input("Group (A, B...)")

    if st.button("Create Group"):
        group_name = f"{grade}{group_letter}"

        c.execute(
            "INSERT INTO groups (name, grade, teacher_id) VALUES (?, ?, ?)",
            (group_name, grade, st.session_state.teacher_id)
        )
        conn.commit()
        st.success("Group created")

    st.subheader("Your Groups")

    c.execute("SELECT * FROM groups WHERE teacher_id=?", (st.session_state.teacher_id,))
    groups = c.fetchall()

    for g in groups:
        st.write(f"Grade {g[2]} - Group {g[1]}")

# ---------------- STUDENTS ----------------
elif menu == "Students":
    st.title("👥 Students")

    c.execute("SELECT * FROM groups WHERE teacher_id=?", (st.session_state.teacher_id,))
    groups = c.fetchall()

    if groups:
        grades = list(set([g[2] for g in groups]))
        selected_grade = st.selectbox("Select Grade", grades)

        filtered_groups = [g for g in groups if g[2] == selected_grade]
        group_names = [g[1] for g in filtered_groups]

        selected_group = st.selectbox("Select Group", group_names)

        group_id = [g[0] for g in filtered_groups if g[1] == selected_group][0]

        student_name = st.text_input("Student name")

        if st.button("Add Student"):
            c.execute(
                "INSERT INTO students (name, group_id) VALUES (?, ?)",
                (student_name, group_id)
            )
            conn.commit()
            st.success("Student added")

        st.subheader("Students List")

        c.execute("SELECT * FROM students WHERE group_id=?", (group_id,))
        students = c.fetchall()

        for s in students:
            st.write(s[1])

# ---------------- ATTENDANCE ----------------
elif menu == "Attendance":
    st.title("✅ Attendance")

    c.execute("SELECT * FROM groups WHERE teacher_id=?", (st.session_state.teacher_id,))
    groups = c.fetchall()

    if groups:
        grades = list(set([g[2] for g in groups]))
        selected_grade = st.selectbox("Grade", grades)

        filtered_groups = [g for g in groups if g[2] == selected_grade]
        group_names = [g[1] for g in filtered_groups]

        selected_group = st.selectbox("Group", group_names)

        group_id = [g[0] for g in filtered_groups if g[1] == selected_group][0]

        c.execute("SELECT * FROM students WHERE group_id=?", (group_id,))
        students = c.fetchall()

        today = datetime.now().strftime("%Y-%m-%d")

        for s in students:
            col1, col2 = st.columns([3,2])
            col1.write(s[1])

            status = col2.radio(
                f"att_{s[0]}",
                ["✔", "❌", "⏰"],
                horizontal=True
            )

            if st.button(f"save_{s[0]}"):
                c.execute(
                    "INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                    (s[0], today, status)
                )
                conn.commit()

        st.success("Attendance saved")
