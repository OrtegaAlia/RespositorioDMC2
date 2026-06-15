import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataAnalyzer:
    """Clase encargada de encapsular la lógica del análisis exploratorio."""
    
    def __init__(self, df):
        self.df = df
        
    def obtener_info_general(self):
        """Retorna un resumen de tipos de datos y valores nulos."""
        info_df = pd.DataFrame({
            'Tipo de Dato': self.df.dtypes.astype(str),
            'Valores No Nulos': self.df.notnull().sum(),
            'Valores Nulos': self.df.isnull().sum()
        })
        return info_df

    def clasificar_variables(self):
        """Función personalizada para agrupar columnas por tipo."""
        numericas = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categoricas = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        return numericas, categoricas

    def obtener_estadisticas(self):
        """Retorna las métricas descriptivas del dataset."""
        return self.df.describe(include='all').transpose()

    def calcular_faltantes(self):
        """Calcula el porcentaje de valores nulos."""
        total_nulos = self.df.isnull().sum()
        porcentaje = (total_nulos / len(self.df)) * 100
        tabla_nulos = pd.DataFrame({'Nulos': total_nulos, 'Porcentaje (%)': porcentaje})
        return tabla_nulos[tabla_nulos['Nulos'] > 0]
