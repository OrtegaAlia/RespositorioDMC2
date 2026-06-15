import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    def __init__(self, df):
        self.df = df     
    def obtener_info_general(self):
        info_df = pd.DataFrame({
            'Tipo de Dato': self.df.dtypes.astype(str),
            'Valores No Nulos': self.df.notnull().sum(),
            'Valores Nulos': self.df.isnull().sum()
        })
        return info_df

    def clasificar_variables(self):
        numericas = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categoricas = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        return numericas, categoricas

    def obtener_estadisticas(self):
        return self.df.describe(include='all').transpose()

    def calcular_faltantes(self):
        total_nulos = self.df.isnull().sum()
        porcentaje = (total_nulos / len(self.df)) * 100
        tabla_nulos = pd.DataFrame({'Nulos': total_nulos, 'Porcentaje (%)': porcentaje})
        return tabla_nulos[tabla_nulos['Nulos'] > 0]

st.set_page_config(page_title="Seguros Analytics App", layout="wide")

st.sidebar.title("Navegación 🧭")
opcion_menu = st.sidebar.radio(
    "Selecciona un módulo:",
    ["Módulo 1: Home", "Módulo 2: Carga del Dataset", "Módulo 3: EDA Core", "Módulo 4: Conclusiones"]
)

if 'data' not in st.session_state:
    st.session_state['data'] = None

if opcion_menu == "Módulo 1: Home":
    st.title("📊 Aplicación Interactiva: Análisis de Renovación de Pólizas")
    st.subheader("Caso de Estudio N°3 - Especialización en Python for Analytics")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 🎯 Objetivo del Proyecto
        Esta plataforma interactiva tiene como fin realizar un **Análisis Exploratorio de Datos (EDA)** 
        sobre el comportamiento de clientes de seguros. El propósito principal es descubrir los factores 
        críticos que influyen en la **renovación de pólizas (`renewal`)**, ayudando a la toma de decisiones comerciales.
        """)
        st.markdown("### 🛠️ Tecnologías Utilizadas")
        st.code("Python | Streamlit | Pandas | NumPy | Matplotlib | Seaborn", language="")
    
    with col2:
        st.info("""
        **🎓 Autor del Proyecto**  
        * **Nombre Completo:** Alia Ortega Alvarado 
        * **Programa:** Especialización en Python for Analytics  
        * **Año:** 2026
        """)
