import streamlit as st
import pandas as pd
import os
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Academic Intelligence System", layout="wide")

st.markdown("## ⚡ Academic Intelligence System 🎮")

DATA_FILE = "data/students.csv"

# =========================
# LOAD
# =========================
if "df" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.df = pd.read_csv(DATA_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=["Nombre", "Puntos", "Grupo"])

df = st.session_state.df

# =========================
# LEVEL SYSTEM
# =========================
def get_level(puntos):
    if puntos >= 10:
        return "🔥 Leyenda"
    elif puntos >= 5:
        return "⭐ Pro"
    elif puntos >= 0:
        return "🙂 Novato"
    else:
        return "⚠️ Riesgo"

def get_color(puntos):
    if puntos >= 10:
        return "#00ff88"
    elif puntos >= 5:
        return "#00c3ff"
    elif puntos >= 0:
        return "#ffaa00"
    else:
        return "#ff4b4b"

# =========================
# UPLOAD
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

        group_name = file.name.split("_")[1] if "_" in file.name else file.name

        temp_df = temp_df.rename(columns={"Estudiante": "Nombre"})

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

    st.success("✅ Datos cargados")

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio("Menu", [
    "🎮 Dashboard",
    "⚡ Control",
    "🚨 Alerts",
    "📊 Reports"
])

if not df.empty:
    grupo_sel = st.sidebar.selectbox("🎯 Grupo", df["Grupo"].unique())
    df = df[df["Grupo"] == grupo_sel]

# =========================
# DASHBOARD PRO
# =========================
if menu == "🎮 Dashboard":

    st.markdown("### 🏆 Ranking del Grupo")

    if not df.empty:

        ranking = df.sort_values("Puntos", ascending=False)

        for _, row in ranking.iterrows():

            level = get_level(row["Puntos"])
            color = get_color(row["Puntos"])

            st.markdown(f"""
            <div style="
                background-color:{color};
                padding:15px;
                border-radius:15px;
                margin-bottom:10px;
                color:black;
                font-weight:bold;
            ">
                🎮 {row['Nombre']} | {row['Puntos']} pts | {level}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        fig = px.bar(
            ranking,
            x="Nombre",
            y="Puntos",
            color="Puntos",
            title="📊 Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================
# CONTROL (BOTONES PRO)
# =========================
elif menu == "⚡ Control":

    st.markdown("### 🎯 Control en Vivo")

    if not df.empty:

        student = st.selectbox("Selecciona alumno", df["Nombre"].unique())

        col1, col2, col3, col4 = st.columns(4)

        if col1.button("➕ +1"):
            delta = 1
        elif col2.button("🔥 +3"):
            delta = 3
        elif col3.button("⚠️ -1"):
            delta = -1
        elif col4.button("💀 -3"):
            delta = -3
        else:
            delta = 0

        if delta != 0:
            idx = st.session_state.df[
                (st.session_state.df["Nombre"] == student) &
                (st.session_state.df["Grupo"] == grupo_sel)
            ].index

            st.session_state.df.loc[idx, "Puntos"] += delta
            st.session_state.df.to_csv(DATA_FILE, index=False)

            st.success(f"{student} → {delta} pts")

# =========================
# ALERTS
# =========================
elif menu == "🚨 Alerts":

    st.markdown("### 🚨 Atención")

    if not df.empty:
        for _, row in df.iterrows():
            if row["Puntos"] < 0:
                st.error(f"{row['Nombre']} necesita intervención")

# =========================
# REPORTS
# =========================
elif menu == "📊 Reports":

    st.markdown("### 📊 Datos")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            "report.csv",
            "text/csv"
        )
