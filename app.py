import streamlit as st
from modules.load_data import load_data
from modules.filters import apply_filters
from modules.metrics import show_metrics
from modules.dashboard import show_dashboard
from modules.alerts import show_alerts
from modules.dojo_view import show_dojo

# CONFIG
st.set_page_config(page_title="Teacher Control Pro", layout="wide")

# LOAD
df = load_data()

# FILTROS
df_filtered = apply_filters(df)

# KPIs
show_metrics(df_filtered)

# DASHBOARD
show_dashboard(df_filtered)

# ALERTAS
show_alerts(df_filtered)

# DOJO VIEW
show_dojo(df_filtered)
