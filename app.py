import streamlit as st
import pandas as pd
import os

# CONFIG
st.set_page_config(page_title="Academic Intelligence System", layout="wide")

st.title("⚡ Academic Intelligence System")

# =========================
# DATA STORAGE
# =========================
DATA_FILE = "data/students.csv"

# =========================
# INIT SESSION
# =========================
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Nombre", "Puntos"])

# =========================
# FILE UPLOADER (MULTIPLE)
# =========================
st.sidebar.header("📂 Load ClassDojo Reports")

uploaded_files = st.sidebar.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    all_dfs = []

    for file in uploaded_files:
        temp_df = pd.read_csv(file)
        all_dfs.append(temp_df)

    merged_df = pd.concat(all_dfs, ignore_index=True)

    # LIMPIEZA BÁSICA (ajusta si cambia formato)
    if "Nombre" in merged_df.columns:
        students = merged_df["Nombre"].unique()
        new_df = pd.DataFrame({
            "Nombre": students,
            "Puntos": [0]*len(students)
        })

        st.session_state.df = new_df

        os.makedirs("data", exist_ok=True)
        st.session_state.df.to_csv(DATA_FILE, index=False)

        st.sidebar.success("✅ Students loaded correctly")

# =========================
# LOAD SAVED DATA
# =========================
if os.path.exists(DATA_FILE):
    st.session_state.df = pd.read_csv(DATA_FILE)

df = st.session_state.df

# =========================
# MENU
# =========================
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Student Intelligence",
    "Alerts Center",
    "Reports"
])

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.header("Overview")

    col1, col2 = st.columns(2)

    if not df.empty:
        col1.metric("Students", df["Nombre"].nunique())
        col2.metric("Total Points", int(df["Puntos"].sum()))
    else:
        col1.metric("Students", 0)
        col2.metric("Total Points", 0)

    st.dataframe(df)

# =========================
# STUDENT INTELLIGENCE
# =========================
elif menu == "Student Intelligence":

    st.header("Student Intelligence")

    if df.empty:
        st.warning("Upload students first")
    else:
        students = df["Nombre"].unique()

        col1, col2 = st.columns(2)

        student = col1.selectbox("Select student", students)

        puntos = col2.number_input("Points (+ / -)", step=1, value=0)

        if st.button("Apply Points ⚡"):

            idx = df[df["Nombre"] == student].index

            if len(idx) > 0:
                st.session_state.df.loc[idx, "Puntos"] += puntos

            os.makedirs("data", exist_ok=True)
            st.session_state.df.to_csv(DATA_FILE, index=False)

            st.success(f"{puntos} points applied to {student}")

# =========================
# ALERTS CENTER
# =========================
elif menu == "Alerts Center":

    st.header("🚨 Alerts Center")

    if df.empty:
        st.warning("No data")
    else
