import streamlit as st
import pandas as pd
import os
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Academic Intelligence System", layout="wide")

st.markdown("## ⚡ Academic Intelligence System")

DATA_FILE = "data/students.csv"

# =========================
# LOAD BASE
# =========================
if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.df = pd.read_csv(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=["Nombre", "Puntos", "Grupo"])

df = st.session_state.df

# =========================
# UPLOAD (CLASDOJO REAL)
# =========================
uploaded_files = st.file_uploader(
    "📂 Upload ClassDojo reports",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    dfs = []

    for file in uploaded_files:
        temp_df = pd.read_csv(file, sep=",", encoding="utf-8-sig")

        # EXTRAER GRUPO DEL NOMBRE
        group_name = file.name.split("_")[1] if "_" in file.name else file.name

        # NOMBRE
        temp_df = temp_df.rename(columns={"Estudiante": "Nombre"})

        # PUNTOS
        positivos = pd.to_numeric(temp_df["Positivo"], errors="coerce").fillna(0)
        negativos = pd.to_numeric(temp_df["Necesita trabajo"], errors="coerce").fillna(0)

        temp_df["Puntos"] = positivos - negativos
        temp_df["Grupo"] = group_name

        temp_df = temp_df[["Nombre", "Puntos", "Grupo"]]

        dfs.append(temp_df)

    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df = combined_df.groupby(["Nombre", "Grupo"], as_index=False).sum()

    st.session_state.df = combined_df
    df = combined_df

    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_FILE, index=False)

    st.success("✅ Datos cargados correctamente")

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Student Intelligence",
    "Alerts Center",
    "Reports"
])

# FILTRO POR GRUPO
if not df.empty:
    grupos = df["Grupo"].unique()
    grupo_sel = st.sidebar.selectbox("🎯 Grupo", grupos)
    df = df[df["Grupo"] == grupo_sel]

# =========================
# DASHBOARD PREMIUM
# =========================
if menu == "Dashboard":

    st.markdown("### 📊 Overview")

    if not df.empty:

        total_students = df["Nombre"].nunique()
        total_points = int(df["Puntos"].sum())
        promedio = int(df["Puntos"].mean())

        col1, col2, col3 = st.columns(3)

        col1.metric("👨‍🎓 Students", total_students)
        col2.metric("⭐ Total Points", total_points)
        col3.metric("📈 Average", promedio)

        st.markdown("---")

        colA, colB = st.columns(2)

        top = df.sort_values("Puntos", ascending=False).head(5)
        risk = df.sort_values("Puntos", ascending=True).head(5)

        with colA:
            st.markdown("### 🏆 Top Students")
            for i, row in top.iterrows():
                st.success(f"{row['Nombre']} → {row['Puntos']} pts")

        with colB:
            st.markdown("### ⚠️ Needs Attention")
            for i, row in risk.iterrows():
                st.error(f"{row['Nombre']} → {row['Puntos']} pts")

        st.markdown("---")

        # 🔥 GRÁFICA IMPACTO
        fig = px.bar(
            df.sort_values("Puntos"),
            x="Nombre",
            y="Puntos",
            color="Puntos",
            title="📊 Student Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================
# STUDENT INTELLIGENCE
# =========================
elif menu == "Student Intelligence":

    st.markdown("### 🎯 Student Control")

    if not df.empty:
        student = st.selectbox("Select student", df["Nombre"].unique())
        puntos = st.number_input("Points (+ / -)", step=1, value=0)

        if st.button("Apply ⚡"):
            idx = st.session_state.df[
                (st.session_state.df["Nombre"] == student) &
                (st.session_state.df["Grupo"] == grupo_sel)
            ].index

            st.session_state.df.loc[idx, "Puntos"] += puntos

            st.session_state.df.to_csv(DATA_FILE, index=False)

            st.success("Updated")

# =========================
# ALERTS CENTER
# =========================
elif menu == "Alerts Center":

    st.markdown("### 🚨 Alerts")

    if not df.empty:
        for _, row in df.iterrows():
            if row["Puntos"] < 0:
                st.error(f"{row['Nombre']} needs attention")

# =========================
# REPORTS
# =========================
elif menu == "Reports":

    st.markdown("### 📊 Reports")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "report.csv",
            "text/csv"
        )
