import streamlit as st

def show_dojo(df):
    st.subheader("🎮 Modo Clase en Vivo")

    updated_rows = []

    for grupo in df["Grupo"].unique():
        st.markdown(f"### 📘 Grupo {grupo}")

        grupo_df = df[df["Grupo"] == grupo]

        for i, row in grupo_df.iterrows():

            col1, col2, col3, col4 = st.columns([3,1,1,1])

            with col1:
                st.markdown(f"**{row['Alumno']}**")

            with col2:
                st.write(f"⭐ {row['Puntos']}")

            # 🔥 BOTÓN SUMAR
            with col3:
                if st.button("➕", key=f"plus_{i}"):
                    row["Puntos"] += 1
                    row["Estado"] = 1

            # 🔥 BOTÓN RESTAR
            with col4:
                if st.button("➖", key=f"minus_{i}"):
                    row["Puntos"] = max(0, row["Puntos"] - 1)

            updated_rows.append(row)

    return df.__class__(updated_rows)
