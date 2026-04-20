import streamlit as st
import pandas as pd
import os
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Academic Intelligence System", layout="wide")
st.markdown("## ⚡ Academic Intelligence System 🎮🧠")

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
# SISTEMA EXPERTO
# =========================
def get_level(p):
    if p >= 10: return "🔥 Leyenda"
    elif p >= 5: return "⭐ Pro"
    elif p >= 0: return "🙂 Novato"
    else: return "⚠️ Riesgo"

def get_status(p):
    if p >= 10: return "Líder"
    elif p >= 5: return "Estable"
    elif p >= 0: return "Atención leve"
    else: return "Riesgo alto"

def decision_engine(p):
    if p >= 10: return "Asignar liderazgo"
    elif p >= 5: return "Refuerzo positivo"
    elif p >= 0: return "Seguimiento cercano"
    else: return "Intervención directa"

def get_color(p):
    if p >= 10: return "#00ff88"
    elif p >= 5: return "#00c3ff"
    elif p >= 0: return "#ffaa00"
    else: return "#ff4b4b"

# =========================
# UPLOAD CLASDOJO REAL
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

        # grupo desde nombre archivo
        grupo = file.name.split("_")[1] if "_" in file.name else file.name

        # columna real
        temp_df = temp_df.rename(columns={"Estudiante": "Nombre"})

        positivos = pd.to_numeric(temp_df["Positivo"], errors="coerce").fillna(0)
        negativos = pd.to_numeric(temp_df["Necesita trabajo"], errors="coerce").fillna(0)

        temp_df["Puntos"] = positivos - negativos
        temp_df["Grupo"] = grupo

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
    "🎮 Dashboard",
    "⚡ Control",
    "🚨 Alerts",
    "📊 Reports"
])

# filtro grupo
if not df.empty:
    grupo_sel = st.sidebar.selectbox("🎯 Grupo", df["Grupo"].unique())
    df = df[df["Grupo"] == grupo_sel]

# =========================
# DASHBOARD EXPERTO
# =========================
if menu == "🎮 Dashboard":

    st.markdown("### 🧠 Sistema Experto del Grupo")

    if not df.empty:

        ranking = df.sort_values("Puntos", ascending=False)

        for _, row in ranking.iterrows():
            p = row["Puntos"]
            st.markdown(f"""
            <div style="
                background-color:{get_color(p)};
                padding:15px;
                border-radius:15px;
                margin-bottom:10px;
                color:black;
            ">
                <b>🎮 {row['Nombre']}</b><br>
                Puntos: {p}<br>
                Nivel: {get_level(p)}<br>
                Estado: {get_status(p)}<br>
                🧠 Acción: {decision_engine(p)}
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
# CONTROL GAMIFICADO
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
# ALERTAS INTELIGENTES
# =========================
elif menu == "🚨 Alerts":

    st.markdown("### 🚨 Alertas Inteligentes")

    if not df.empty:

        riesgo = df[df["Puntos"] < 0]
        lideres = df[df["Puntos"] >= 10]

        st.markdown("#### ⚠️ Riesgo alto")
        for _, row in riesgo.iterrows():
            st.error(f"{row['Nombre']} → intervención inmediata")

        st.markdown("#### 🏆 Líderes")
        for _, row in lideres.iterrows():
            st.success(f"{row['Nombre']} → líder del grupo")

# =========================
# REPORTES
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
