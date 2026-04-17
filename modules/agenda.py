import streamlit as st
import pandas as pd
from datetime import date
import os

def agenda_ui():
    st.header("📅 Agenda")

    evento = st.text_input("Evento")
    fecha = st.date_input("Fecha", value=date.today())

    if st.button("Agregar evento"):
        data = {"Evento": evento, "Fecha": fecha}
        df = pd.DataFrame([data])

        if os.path.exists("data/agenda.csv"):
            df_old = pd.read_csv("data/agenda.csv")
            df = pd.concat([df_old, df])

        df.to_csv("data/agenda.csv", index=False)
        st.success("Evento guardado")

    if os.path.exists("data/agenda.csv"):
        st.subheader("Eventos")
        st.dataframe(pd.read_csv("data/agenda.csv"))
