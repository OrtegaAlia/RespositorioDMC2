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
