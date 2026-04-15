import pandas as pd

def load_data():
    df = pd.read_csv("data/Log_Unificado.csv")

    df["Estado"] = df["Estado"].fillna(0).astype(int)
    df["Puntos"] = df["Puntos"].fillna(0)

    df["Alumno"] = df["Alumno"].astype(str)

    return df
