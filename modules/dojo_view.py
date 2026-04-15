import streamlit as st

def show_dojo(df):
    st.subheader("Vista tipo ClassDojo")

    grupos = df["Grupo"].unique()

    for grupo in grupos:
        st.markdown(f"### Grupo {grupo}")

        grupo_df = df[df["Grupo"] == grupo]

        cols = st.columns(5)

        for i, row in grupo_df.iterrows():
            color = "#00FF9C" if row["Estado"] == 1 else "#FF4B4B"

            cols[i % 5].markdown(
                f"""
                <div style="
                    background-color: {color};
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                ">
                    <b>{row['Alumno']}</b><br>
                    ⭐ {row['Puntos']}
                </div>
                """,
                unsafe_allow_html=True
            )
