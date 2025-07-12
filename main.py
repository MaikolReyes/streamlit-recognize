import streamlit as st # type: ignore
import pandas as pd
import openai
from dotenv import load_dotenv # type: ignore
import os

# Cargar clave API
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("🔍 Generador de Insights Automáticos con IA")

# Subida del archivo
file = st.file_uploader("Subí tu archivo CSV", type="csv")

if file:
    df = pd.read_csv(file)
    st.subheader("Vista previa del dataset")
    st.dataframe(df.head())

    # Análisis básico con pandas
    st.subheader("Resumen estadístico")
    st.dataframe(df.describe(include='all').T)

    # Enviar a GPT
    if st.button("Generar insights con IA"):
        prompt = f"""
        Actuá como un analista de datos. A partir de este resumen estadístico:

        {df.describe(include='all').to_string()}

        Generá un informe con insights clave sobre el comportamiento de los datos. 
        Escribílo en lenguaje claro y profesional.
        """

        with st.spinner("Generando análisis con IA..."):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            insights = response["choices"][0]["message"]["content"]
        
        st.subheader("🧠 Insights generados")
        st.write(insights)
        st.success("Insights generados exitosamente.")
else:
    st.info("Por favor, subí un archivo CSV para comenzar.")