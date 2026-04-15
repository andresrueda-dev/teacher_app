import pandas as pd
import os

def load_data():
    file_path = os.path.join("data", "Log_Unificado.csv")

    if not os.path.exists(file_path):
        return pd.DataFrame({
            "Alumno": ["SIN DATA"],
            "Grupo": ["NA"],
            "Equipo": [0],
            "Puntos": [0],
            "Nivel": ["🔴"],
            "Estado": [0]
        })

    df = pd.read_csv(file_path)

    df["Estado"] = pd.to_numeric(df["Estado"], errors="coerce").fillna(0).astype(int)
    df["Puntos"] = pd.to_numeric(df["Puntos"], errors="coerce").fillna(0)

    return df
