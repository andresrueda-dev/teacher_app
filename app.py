import streamlit as st
import pandas as pd
import pandas as pd

def guardar_datos(df):
    df.to_csv("alumnos.csv", index=False)

def cargar_datos():
    try:
        return pd.read_csv("alumnos.csv")
    except:
        return pd.DataFrame()
st.title("📚 Class Manager")

opcion = st.selectbox("Selecciona una opción", [
    "Crear clase",
    "Importar lista",
    "Ver alumnos"
])
import os

if st.button("🔄 Restablecer sistema"):
    if os.path.exists("alumnos.csv"):
        os.remove("alumnos.csv")
    st.warning("Sistema reiniciado")
import shutil

def backup():
    if os.path.exists("alumnos.csv"):
        shutil.copy("alumnos.csv", "backup_alumnos.csv")
        
if st.button("♻️ Recuperar respaldo"):
    if os.path.exists("backup_alumnos.csv"):
        shutil.copy("backup_alumnos.csv", "alumnos.csv")
        st.success("Datos recuperados")
        
if opcion == "Crear clase":
    nombre_clase = st.text_input("Nombre de la clase")
    if st.button("Crear"):
        st.success(f"Clase '{nombre_clase}' creada")

elif opcion == "Importar lista":
    archivo = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

    if archivo:
        df = pd.read_excel(archivo)
        st.write("Vista previa:")
        st.dataframe(df)

        if st.button("Guardar lista"):
            st.success("Lista importada correctamente")

elif opcion == "Ver alumnos":
    st.info("Aquí se mostrarán los alumnos guardados")
