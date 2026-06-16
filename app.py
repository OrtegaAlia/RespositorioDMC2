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

st.sidebar.image("Logo_insurance.png")

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

elif opcion_menu == "Módulo 2: Carga del Dataset":
    st.title("📂 Gestión e Ingreso de Datos")
    st.write("Sube el archivo `InsuranceCompany.csv` para iniciar el procesamiento automatizado.")
    
    archivo_cargado = st.sidebar.file_uploader("Selecciona el archivo CSV de la aseguradora", type=["csv"])
    
    if archivo_cargado is not None:
        try:
            df = pd.read_csv(archivo_cargado)
            st.session_state['data'] = df
            st.success("✅ ¡El dataset se cargó correctamente!")
            
            # Métricas dinámicas utilizando st.columns
            m1, m2 = st.columns(2)
            m1.metric("Número de Registros (Filas)", f"{df.shape[0]:,}")
            m2.metric("Total de Variables (Columnas)", df.shape[1])
            
            st.markdown("### 🔍 Vista Previa de los Datos (Primeras filas)")
            st.dataframe(df.head(10))
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    else:
        st.warning("⚠️ Esperando la carga del archivo CSV en el panel superior.")

elif opcion_menu == "Módulo 3: EDA Core":
    if st.session_state['data'] is None:
        st.error("❌ No hay datos disponibles. Por favor, sube el archivo en el **Módulo 2**.")
    else:
        df = st.session_state['data']
        analyzer = DataAnalyzer(df)
        num_cols, cat_cols = analyzer.clasificar_variables()
        
        st.title("🧠 Núcleo de Análisis Exploratorio de Datos (EDA)")
        st.write("Usa las pestañas inferiores para explorar los 10 ítems analíticos requeridos.")
        
        # Estructura obligatoria mediante Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Diagnóstico Base (Ítems 1-3)", 
            "⚠️ Faltantes y Distribución (Ítems 4-5)", 
            "🗂️ Categóricos (Ítem 6)", 
            "🔗 Cruces Bivariados (Ítems 7-8)", 
            "🎛️ Panel Dinámico e Insights (Ítems 9-10)"
        ])
        
        # --- TAB 1 ---
        with tab1:
            st.header("Ítem 1: Información General del Dataset")
            st.dataframe(analyzer.obtener_info_general())
            
            st.header("Ítem 2: Clasificación de Variables")
            c1, c2 = st.columns(2)
            c1.write(f"**Variables Numéricas ({len(num_cols)}):**")
            c1.write(num_cols)
            c2.write(f"**Variables Categóricas ({len(cat_cols)}):**")
            c2.write(cat_cols)
            
            st.header("Ítem 3: Estadísticas Descriptivas")
            st.dataframe(analyzer.obtener_estadisticas())
            st.write("**Interpretación:** Observa las medias y las medianas. Desviaciones estándar altas sugieren una gran dispersión de ingresos.")

        # --- TAB 2 ---
        with tab2:
            st.header("Ítem 4: Análisis de Valores Faltantes")
            tabla_nulos = analyzer.calcular_faltantes()
            if not tabla_nulos.empty:
                st.dataframe(tabla_nulos)
                st.write("**Discusión:** Los valores nulos deben tratarse mediante imputación o eliminación antes de construir cualquier modelo.")
            else:
                st.success("¡Perfecto! No se encontraron valores faltantes en el set de datos.")
                
            st.header("Ítem 5: Distribución de Variables Numéricas")
            var_num_sel = st.selectbox("Elige una variable numérica para graficar:", num_cols, key="num_dist")
            
            fig, ax = plt.subplots(figsize=(7, 3.5))
            sns.histplot(df[var_num_sel].dropna(), kde=True, color="skyblue", ax=ax)
            ax.set_title(f"Distribución de: {var_num_sel}")
            st.pyplot(fig)

        # --- TAB 3 ---
        with tab3:
            st.header("Ítem 6: Análisis de Variables Categóricas")
            var_cat_sel = st.selectbox("Elige una variable categórica para analizar:", cat_cols, key="cat_dist")
            
            conteos = df[var_cat_sel].value_counts()
            proporciones = df[var_cat_sel].value_counts(normalize=True) * 100
            
            resumen_cat = pd.DataFrame({'Conteo Absoluto': conteos, 'Proporción (%)': proporciones})
            st.dataframe(resumen_cat)
            
            fig, ax = plt.subplots(figsize=(7, 3.5))
            sns.barplot(x=conteos.index, y=conteos.values, palette="muted", ax=ax)
            ax.set_title(f"Frecuencia de la variable {var_cat_sel}")
            st.pyplot(fig)

        # --- TAB 4 ---
        with tab4:
            st.header("Ítem 7: Análisis Bivariado (Numérico vs Categórico)")
            st.write("Evaluación de factores numéricos frente a la renovación (`renewal`).")
            var_biv_num = st.selectbox("Selecciona la métrica numérica:", num_cols, index=min(3, len(num_cols)-1))
            
            fig, ax = plt.subplots(figsize=(7, 4))
            # Tratamos de cruzarlo con 'renewal' si existe en las categóricas
            target_col = 'renewal' if 'renewal' in df.columns else cat_cols[0]
            sns.boxplot(x=target_col, y=var_biv_num, data=df, palette="Set2", ax=ax)
            ax.set_title(f"Análisis de {var_biv_num} según estado de {target_col}")
            st.pyplot(fig)
            
            st.header("Ítem 8: Análisis Bivariado (Categórico vs Categórico)")
            var_biv_cat = st.selectbox("Selecciona otra variable categórica:", [c for c in cat_cols if c != 'renewal'])
            
            target_col = 'renewal' if 'renewal' in df.columns else cat_cols[0]
            tabla_cruzada = pd.crosstab(df[var_biv_cat], df[target_col], normalize='index') * 100
            st.write("Tabla de contingencia (Porcentajes por fila):")
            st.dataframe(tabla_cruzada)
            
            fig, ax = plt.subplots(figsize=(7, 4))
            tabla_cruzada.plot(kind='bar', stacked=True, color=['#e74c3c', '#2ecc71'], ax=ax)
            ax.set_ylabel("Porcentaje %")
            st.pyplot(fig)

        # --- TAB 5 ---
        with tab5:
            st.header("Ítem 9: Análisis Basado en Parámetros Seleccionados")
            columnas_usuario = st.multiselect("Elige las columnas que deseas extraer del dataset dinámicamente:", df.columns.tolist(), default=df.columns.tolist()[:3])
            
            if columnas_usuario:
                filtro_slider = st.slider("Filtrar registros a visualizar (Muestra):", 5, min(100, len(df)), 20)
                st.dataframe(df[columnas_usuario].head(filtro_slider))
