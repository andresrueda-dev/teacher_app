import streamlit as st

def apply_filters(df):
    st.sidebar.header("Filtros")

    grupos = sorted(df["Grupo"].dropna().unique())

    grupo = st.sidebar.selectbox("Grupo", ["Todos"] + list(grupos))

    if grupo != "Todos":
        df = df[df["Grupo"] == grupo]

    buscar = st.sidebar.text_input("Buscar alumno")

    if buscar:
        df = df[df["Alumno"].str.contains(buscar, case=False, na=False)]

    return df
