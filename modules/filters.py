import streamlit as st

def apply_filters(df):
    st.sidebar.header("🎯 Filtros")

    grupo = st.sidebar.selectbox("Grupo", ["Todos"] + sorted(df["Grupo"].unique()))

    if grupo != "Todos":
        df = df[df["Grupo"] == grupo]

    buscar = st.sidebar.text_input("Buscar alumno")

    if buscar:
        df = df[df["Alumno"].str.contains(buscar, case=False)]

    return df
