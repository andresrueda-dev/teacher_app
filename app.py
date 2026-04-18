import streamlit as st
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="Teacher Intelligence System", layout="wide")

# =========================
# 🎯 DATA BASE (SIMULADA + REALISTA)
# =========================
students = [
    {"name": "ASHELY AIDEE", "last_login": None},
    {"name": "AXEL TORRES", "last_login": "2026-01-30"},
    {"name": "DANIEL QUINTANA", "last_login": "2026-01-28"},
    {"name": "EDUARDO VILCHIS", "last_login": "2026-03-20"},
    {"name": "EMILIANO LUNA", "last_login": None},
    {"name": "EVOLETH ANALY", "last_login": None},
    {"name": "FERNANDA AMAYA", "last_login": "2026-02-25"},
    {"name": "GAEL GALICIA", "last_login": "2026-02-06"},
    {"name": "GRETEL ALEJANDRA", "last_login": "2026-02-02"},
    {"name": "GUSTAVO ANGEL", "last_login": "2026-01-30"},
    {"name": "HARUMI CALIXTO", "last_login": "2026-02-18"},
    {"name": "IKER IRÁN", "last_login": None},
    {"name": "INGRID XIMENA", "last_login": "2026-02-26"},
    {"name": "JESÚS ADRIAN", "last_login": None},
    {"name": "JOALY MENDEZ", "last_login": "2026-02-18"},
    {"name": "LIZETH MARIANA", "last_login": "2026-03-10"},
    {"name": "LUIS DAVID", "last_login": None},
    {"name": "LUIS GERARDO", "last_login": "2026-02-19"},
    {"name": "MARIANA FALOFUL", "last_login": "2026-04-04"},
    {"name": "ZOE RANGEL", "last_login": None}
]

# =========================
# 🧠 LÓGICA INTELIGENTE
# =========================
def classify_student(last_login):
    if last_login is None:
        return "critical"
    last = datetime.strptime(last_login, "%Y-%m-%d")
    days = (datetime.now() - last).days

    if days <= 7:
        return "active"
    elif days <= 30:
        return "risk"
    else:
        return "critical"

def generate_metrics(category):
    if category == "active":
        return {
            "tasks": random.randint(7,10),
            "participation": random.randint(80,100),
            "grade": random.randint(85,100),
            "risk_fail": "Low"
        }
    elif category == "risk":
        return {
            "tasks": random.randint(4,7),
            "participation": random.randint(50,79),
            "grade": random.randint(60,84),
            "risk_fail": "Medium"
        }
    else:
        return {
            "tasks": random.randint(0,4),
            "participation": random.randint(10,49),
            "grade": random.randint(0,59),
            "risk_fail": "High"
        }

# =========================
# 📊 CREACIÓN DATAFRAME
# =========================
data = []
for s in students:
    category = classify_student(s["last_login"])
    metrics = generate_metrics(category)

    data.append({
        "Name": s["name"],
        "Last Login": s["last_login"] if s["last_login"] else "No login",
        "Status": category,
        "Tasks Completed": metrics["tasks"],
        "Participation %": metrics["participation"],
        "Estimated Grade": metrics["grade"],
        "Fail Risk": metrics["risk_fail"]
    })

df = pd.DataFrame(data)

# =========================
# 🎨 HEADER
# =========================
st.title("🎯 Teacher Intelligence Dashboard")
st.subheader("Sistema estratégico de monitoreo académico | Strategic Academic Monitoring System")

# =========================
# 📊 KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Students", len(df))
col2.metric("Active", len(df[df["Status"]=="active"]))
col3.metric("At Risk", len(df[df["Status"]=="risk"]))
col4.metric("Critical", len(df[df["Status"]=="critical"]))

# =========================
# 🎯 FILTRO
# =========================
filter_option = st.selectbox(
    "Filter / Filtro",
    ["all", "active", "risk", "critical"]
)

if filter_option != "all":
    filtered_df = df[df["Status"] == filter_option]
else:
    filtered_df = df

# =========================
# 📋 TABLA PRINCIPAL
# =========================
st.dataframe(filtered_df, use_container_width=True)

# =========================
# 🧠 ALERTAS INTELIGENTES
# =========================
st.subheader("⚠️ Smart Alerts / Alertas Inteligentes")

critical_students = df[df["Status"] == "critical"]

for _, row in critical_students.iterrows():
    st.error(f"🚨 {row['Name']} → HIGH RISK of failing / ALTO RIESGO de reprobación")

# =========================
# 📩 MENSAJES AUTOMÁTICOS
# =========================
st.subheader("📩 Suggested Actions / Acciones sugeridas")

def generate_message(status):
    if status == "critical":
        return "URGENT: You must log in and submit pending tasks immediately."
    elif status == "risk":
        return "Reminder: Please log in this week and complete your activities."
    else:
        return "Great job! Keep it up."

for _, row in filtered_df.iterrows():
    msg = generate_message(row["Status"])
    st.info(f"{row['Name']} → {msg}")

# =========================
# 📈 VISUAL SIMPLE
# =========================
st.subheader("📈 Participation Overview")

st.bar_chart(df.set_index("Name")["Participation %"])
