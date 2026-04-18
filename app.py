import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# =========================
# 🎯 SIDEBAR (NAVEGACIÓN)
# =========================
menu = st.sidebar.radio("Menu", [
    "Dashboard",
    "Student Intelligence",
    "Alerts Center",
    "Reports"
])

st.title("⚡ Academic Intelligence System")

# =========================
# 📊 DASHBOARD
# =========================
if menu == "Dashboard":
    st.subheader("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Students", len(df))
    col2.metric("Critical", len(df[df["AI_Status"]=="CRITICAL"]))
    col3.metric("Risk", len(df[df["AI_Status"]=="RISK"]))
    col4.metric("Avg Grade", int(df["Grade"].mean()))

# =========================
# 📋 STUDENT INTELLIGENCE
# =========================
elif menu == "Student Intelligence":
    st.subheader("Student Analysis")

    def highlight(val):
        if val == "CRITICAL":
            return "background-color:red; color:white"
        elif val == "RISK":
            return "background-color:orange"
        return "background-color:green; color:white"

    st.dataframe(
        df.style.applymap(highlight, subset=["AI_Status"]),
        use_container_width=True
    )

# =========================
# ⚠️ ALERT CENTER
# =========================
elif menu == "Alerts Center":
    st.subheader("Critical Students")

    critical = df[df["AI_Status"]=="CRITICAL"]

    for _, row in critical.iterrows():
        st.error(f"{row['Name']} ({row['Group']}) → {row['Action']}")

# =========================
# 📄 REPORTS
# =========================
elif menu == "Reports":
    st.subheader("Export Data")

    st.download_button(
        "Download CSV Report",
        df.to_csv(index=False),
        file_name="academic_report.csv",
        mime="text/csv"
    )
