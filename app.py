import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Academic Intelligence System", layout="wide")
st.title("⚡ Academic Intelligence System")

DATA_FILE = "data/students.csv"

# =========================
# LOAD BASE DATA
# =========================
if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.df = pd.read_csv(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=["Nombre", "Puntos"])

df = st.session_state.df

# =========================
# READ CSV SAFE (CLASDOJO FIX)
# =========================
def read_csv_safe(file):
    try:
        return pd.read_csv(file, sep=",", encoding="utf-8")
    except:
        try:
            return pd.read_csv(file, sep=";", encoding="latin-1")
        except:
            return pd.read_csv(file)

# =========================
# FIND NAME COLUMN (ROBUSTO)
# =========================
def get_name_column(df):
    cols = [c.lower() for c in df.columns]

    for i, c in enumerate(cols):
        if "student" in c or "name" in c or "nombre" in c:
            return df.columns[i]

    # caso: first + last name
    if "first name" in cols and "last name" in cols:
        df["Nombre"] = df["First name"] + " " + df["Last name"]
        return "Nombre"

    return None

# =========================
# MULTI FILE UPLOADER
# =========================
uploaded_files = st.file_uploader(
    "Upload ClassDojo reports",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    dfs = []

    for file in uploaded_files:
        temp_df = read_csv_safe(file)

        name_col = get_name_column(temp_df)

        if name_col is None:
            st.error(f"❌ No se detectó columna de nombre en {file.name}")
            st.write(list(temp_df.columns))
            continue

        temp_df = temp_df.rename(columns={name_col: "Nombre"})

        # =========================
        # DETECTAR PUNTOS
        # =========================
        temp_df["Puntos"] = 0

        for col in temp_df.columns:
            col_lower = col.lower()

            if "positivo" in col_lower or "positive" in col_lower:
                temp_df["Puntos"] += pd.to_numeric(temp_df[col], errors="coerce").fillna(0)

            if "negativo" in col_lower or "needs" in col_lower:
                temp_df["Puntos"] -= pd.to_numeric(temp_df[col], errors="coerce").fillna(0)

        temp_df = temp_df[["Nombre", "Puntos"]]

        dfs.append(temp_df)

    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df = combined_df.groupby("Nombre", as_index=False).sum()

        st.session_state.df = combined_df

        os.makedirs("data", exist_ok=True)
        combined_df.to_csv(DATA_FILE, index=False)

        df = combined_df

        st.success("✅ Archivos cargados correctamente")

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
        st.warning("No data")
    else:
        student = st.selectbox("Select student", df["Nombre"].unique())
        puntos = st.number_input("Points (+ / -)", step=1, value=0)

        if st.button("Apply ⚡"):
            idx = df[df["Nombre"] == student].index

            st.session_state.df.loc[idx, "Puntos"] += puntos

            os.makedirs("data", exist_ok=True)
            st.session_state.df.to_csv(DATA_FILE, index=False)

            st.success("Updated")

# =========================
# ALERTS
# =========================
elif menu == "Alerts Center":
    st.header("🚨 Alerts")

    if not df.empty:
        for _, row in df.iterrows():
            if row["Puntos"] < 0:
                st.error(f"{row['Nombre']} needs attention")

# =========================
# REPORTS
# =========================
elif menu == "Reports":
    st.header("Reports")

    if not df.empty:
        st.dataframe(df)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "report.csv",
            "text/csv"
        )
