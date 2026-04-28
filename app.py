import streamlit as st
import json
import os

st.set_page_config(page_title="Teacher App PRO", layout="wide")

st.title("📱 Teacher App PRO")

DATA_FILE = "students.json"

# -------- LOAD DATA --------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# -------- SAVE DATA --------
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# -------- SESSION --------
if "students" not in st.session_state:
    st.session_state.students = load_data()

# -------- SIDEBAR --------
st.sidebar.title("Menu")
menu = st.sidebar.radio("Go to", ["Home", "Points", "Ranking", "Reset"])

# -------- HOME --------
if menu == "Home":
    st.header("➕ Add Students")

    col1, col2 = st.columns(2)

    # ---- Add one ----
    with col1:
        st.subheader("Add one student")
        new_student = st.text_input("Student name")

        if st.button("Add student"):
            if new_student:
                st.session_state.students.append({
                    "name": new_student,
                    "points": 0
                })
                save_data(st.session_state.students)
                st.success(f"{new_student} added!")

    # ---- Add multiple ----
    with col2:
        st.subheader("Paste list")
        bulk_students = st.text_area("One name per line")

        if st.button("Add list"):
            if bulk_students:
                names = bulk_students.split("\n")
                for name in names:
                    name = name.strip()
                    if name:
                        st.session_state.students.append({
                            "name": name,
                            "points": 0
                        })
                save_data(st.session_state.students)
                st.success("Students added!")

    st.subheader("📋 Current Students")

    for s in st.session_state.students:
        st.write(f"{s['name']} - {s['points']} pts")

# -------- POINTS --------
elif menu == "Points":
    st.header("🎯 Give Points")

    if not st.session_state.students:
        st.warning("Add students first")
    else:
        for i, student in enumerate(st.session_state.students):
            col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])

            col1.write(student["name"])
            col2.write(f"{student['points']} pts")

            if col3.button("+1", key=f"add1_{i}"):
                st.session_state.students[i]["points"] += 1
                save_data(st.session_state.students)

            if col4.button("+5", key=f"add5_{i}"):
                st.session_state.students[i]["points"] += 5
                save_data(st.session_state.students)

            if col5.button("-1", key=f"sub1_{i}"):
                st.session_state.students[i]["points"] -= 1
                save_data(st.session_state.students)

# -------- RANKING --------
elif menu == "Ranking":
    st.header("🏆 Ranking")

    sorted_students = sorted(
        st.session_state.students,
        key=lambda x: x["points"],
        reverse=True
    )

    for i, student in enumerate(sorted_students, start=1):
        st.write(f"{i}. {student['name']} - {student['points']} pts")

# -------- RESET --------
elif menu == "Reset":
    st.header("⚠️ Reset Data")

    if st.button("Delete ALL data"):
        st.session_state.students = []
        save_data([])
        st.success("All data deleted")
