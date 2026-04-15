import streamlit as st

def show_dashboard(df):
    st.subheader("Rendimiento por grupo")

    data = df.groupby("Grupo")["Estado"].mean()

    st.bar_chart(data)

    st.subheader("Ranking")

    ranking = df.sort_values(by="Puntos", ascending=False)

    st.dataframe(ranking, use_container_width=True)
