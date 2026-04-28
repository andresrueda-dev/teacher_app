import streamlit as st
import sqlite3

st.set_page_config(page_title="Teacher SaaS PRO", layout="wide")

# -------- DB --------
conn = sqlite3.connect("school.db", check_same_thread=False)
c = conn.cursor()

# -------- TABLES --------
c.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    teacher_id INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    points INTEGER,
    group_id INTEGER
)
""")

conn.commit()

# -------- SESSION --------
if "teacher_id" not in st.session_state:
    st.session_state.teacher_id = None

if "group_id" not in st.session_state:
    st.session_state.group_id = None

# -------- LOGIN --------
st.sidebar.title("🔐 Login")

c.execute("SELECT id, name FROM teachers")
teachers = c.fetchall()

teacher_names = [t[1] for t in teachers]

if teacher_names:
    selected_teacher = st.sidebar.selectbox("Select Teacher", teacher_names)

    for t in teachers:
        if t[1] == selected_teacher:
            st.session_state.teacher_id = t[0]
else:
    st.sidebar.warning("Create a teacher first")

# -------- BLOCK IF NO LOGIN --------
if st.session_state.teacher_id is None:
    st.title("⚠️ Setup Required")
    new_teacher = st.text_input("Create Teacher Name")

    if st.button("Create Teacher"):
        if new_teacher:
            c.execute("INSERT INTO teachers (name) VALUES (?)", (new_teacher,))
            conn.commit()
            st.success("Teacher created. Reload app.")

    st.stop()

# -------- SIDEBAR MENU --------
menu = st.sidebar.radio("Menu", ["Groups", "Class", "Ranking"])

st.title("📱 Teacher SaaS PRO")

# -------- GROUPS --------
if menu == "Groups":
    st.header("📚 Manage Groups")

    new_group = st.text_input("New group (1A, 2B...)")

    if st.button("Create group"):
        c.execute(
            "INSERT INTO groups (name, teacher_id) VALUES (?, ?)",
            (new_group, st.session_state.teacher_id)
        )
        conn.commit()
        st.success("Group created")

    # Show groups
    c.execute(
        "SELECT id, name FROM groups WHERE teacher_id=?",
        (st.session_state.teacher_id,)
    )
    groups = c.fetchall()

    st.subheader("Your Groups")
    for g in groups:
        st.write(g[1])

    # Upload students
    st.subheader("➕ Upload Students")
    selected_group_name = st.selectbox(
        "Select group",
        [g[1] for g in groups] if groups else []
    )

    group_id = None
    for g in groups:
        if g[1] == selected_group_name:
            group_id = g[0]

    bulk = st.text_area("Paste students (one per line)")

    if st.button("Upload list"):
        if group_id and bulk:
            for name in bulk.split("\n"):
                name = name.strip()
                if name:
                    c.execute(
                        "INSERT INTO students (name, points, group_id) VALUES (?, 0, ?)",
                        (name, group_id)
                    )
            conn.commit()
            st.success("Students added")

# -------- CLASS --------
elif menu == "Class":
    st.header("🎯 Live Class")

    c.execute(
        "SELECT id, name FROM groups WHERE teacher_id=?",
        (st.session_state.teacher_id,)
    )
    groups = c.fetchall()

    if not groups:
        st.warning("Create a group first")
        st.stop()

    group_names = [g[1] for g in groups]

    selected_group = st.selectbox("Select group", group_names)

    for g in groups:
        if g[1] == selected_group:
            st.session_state.group_id = g[0]

    c.execute(
        "SELECT id, name, points FROM students WHERE group_id=?",
        (st.session_state.group_id,)
    )
    students = c.fetchall()

    for s in students:
        col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])

        col1.write(s[1])
        col2.write(f"{s[2]} pts")

        if col3.button("+1", key=f"add1_{s[0]}"):
            c.execute("UPDATE students SET points = points + 1 WHERE id=?", (s[0],))
            conn.commit()

        if col4.button("+5", key=f"add5_{s[0]}"):
            c.execute("UPDATE students SET points = points + 5 WHERE id=?", (s[0],))
            conn.commit()

        if col5.button("-1", key=f"sub1_{s[0]}"):
            c.execute("UPDATE students SET points = points - 1 WHERE id=?", (s[0],))
            conn.commit()

# -------- RANKING --------
elif menu == "Ranking":
    st.header("🏆 Ranking")

    c.execute(
        """
        SELECT students.name, students.points
        FROM students
        JOIN groups ON students.group_id = groups.id
        WHERE groups.teacher_id=?
        ORDER BY students.points DESC
        """,
        (st.session_state.teacher_id,)
    )

    ranking = c.fetchall()

    for i, s in enumerate(ranking, start=1):
        st.write(f"{i}. {s[0]} - {s[1]} pts")
