import streamlit as st
from modules.load_data import load_data
from modules.filters import apply_filters
from modules.metrics import show_metrics
from modules.dashboard import show_dashboard
from modules.alerts import show_alerts
from modules.dojo_view import show_dojo

st.set_page_config(page_title="Teacher Control Pro", layout="wide")

st.title("📊 Teacher Control System")
st.caption("Nivel PRO - ClassDojo Style")

# Cargar datos
df = load_data()

# Filtros
df = apply_filters(df)

# KPIs
show_metrics(df)

st.divider()

# Dashboard
show_dashboard(df)

st.divider()

# Alertas
show_alerts(df)

st.divider()

# Vista visual
show_dojo(df)
