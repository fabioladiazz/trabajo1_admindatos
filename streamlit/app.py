import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# Configuración de la página
st.set_page_config(page_title='Modelo para predicción de niveles de obesidad', page_icon='🩺', layout='wide')

# Colores base basados en la imagen
BACKGROUND_COLOR = '#F4C7CC'
BORDER_COLOR = '#FF6F61'
TEXT_COLOR = '#333333'

# Estilos CSS personalizados
st.markdown(f"""
    <style>
    .main-container {{
        background-color: {BACKGROUND_COLOR};
        padding: 20px;
        border-radius: 10px;
        border: 2px solid {BORDER_COLOR};
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }}
    h1, h2, p {{
        color: {TEXT_COLOR};
    }}
    </style>
""", unsafe_allow_html=True)

# Imagen principal
image_path = 'C:/Dev/Administración de Datos/FotoPrincipal.jpg'
image = Image.open(image_path)
st.image(image, use_column_width=True)

# Título y subtítulo centrados en toda la página
st.markdown('<h1 style="font-weight: bold; text-align: left;">Modelo para predicción de niveles de obesidad</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 18px; text-align: left;"> Fabiola Díaz, Valerie Espinoza y Alejandro Ocampo</p>', unsafe_allow_html=True)
# Tabs de navegación
tab2, tab3, tab4 = st.tabs(['Data Pipeline', 'Predicciones y Métricas', 'Deployment'])

with tab3:
    st.title('Predicciones y Métricas del Modelo de Predicción de Obesidad')
    
    # Análisis de las imágenes en el orden correcto
    st.header('1. Matriz de Correlación entre Variables Numéricas')
    image_path = 'C:/Dev/Administración de Datos/Matriz.png'
    image = Image.open(image_path)
    st.image(image, caption='Matriz de Correlación entre Variables Numéricas')

    st.header('2. Box Plots para las Variables Continuas')
    image_path = 'C:/Dev/Administración de Datos/VariablesContinuas.png'
    image = Image.open(image_path)
    st.image(image, caption='Box Plots para las Variables Continuas')

    st.header('3. Conteo para las Variables Categóricas')
    image_path = 'C:/Dev/Administración de Datos/VariablesCategoricas.png'
    image = Image.open(image_path)
    st.image(image, caption='Distribución de las Variables Categóricas')

    st.header('4. Distribución de la Variable Objetivo (Obesity)')
    image_path = 'C:/Dev/Administración de Datos/DistribucionVariableObesity.png'
    image = Image.open(image_path)
    st.image(image, caption='Distribución de la Variable Obesity')

    # Tablas de métricas por modelo
    st.header('5. Métricas de Clasificación por Modelo')

    metrics_data = {
        'Modelo': ['XGBoost', 'RandomForest', 'GradientBoosting'],
        'Precisión Promedio': [0.8278, 0.8508, 0.8490],
        'Recall Promedio': [0.8251, 0.8429, 0.8440],
        'F1-Score Promedio': [0.8262, 0.8447, 0.8448],
        'Exactitud': [0.8274, 0.8440, 0.8440]
    }

    df_metrics = pd.DataFrame(metrics_data)
    st.table(df_metrics)

    st.write('El modelo RandomForest es la mejor opción a causa de su alta precisión (0.8508), recall (0.8429) y F1-Score (0.8447).')

    st.header('6. Matriz de Confusión para RandomForest')
    image_path = 'C:/Dev/Administración de Datos/RandomForestMatriz.png'
    image = Image.open(image_path)
    st.image(image, caption='Matriz de Confusión para RandomForest')

    # Tabla final con métricas detalladas del mejor modelo
    st.header('7. Métricas Detalladas del Mejor Modelo (RandomForest)')
    detailed_metrics = {
        'Clase': ['0', '1', '2', '3', '4', '5', '6'],
        'Precisión': [1.00, 0.83, 0.95, 0.96, 0.98, 0.99, 0.99],
        'Recall': [0.93, 0.99, 0.86, 0.94, 0.98, 0.97, 0.99],
        'F1-Score': [0.96, 0.90, 0.91, 0.95, 0.98, 0.98, 0.99],
        'Soporte': [68, 72, 73, 72, 88, 74, 81]
    }

    df_detailed = pd.DataFrame(detailed_metrics)
    st.table(df_detailed)

    st.write('El modelo RandomForest mantiene un rendimiento alto en las métricas generales, al ofrecer consistencia sólida en todas las clases.')

with tab4:
    st.title('Deployment: Predicción de Niveles de Obesidad')
    st.write('Ingrese los valores en los campos a continuación para obtener una predicción del modelo.')

    # Cargar el modelo entrenado
    modelo_path = 'C:/Dev/Administración de Datos/modelo_final.pkl'
    with open(modelo_path, 'rb') as file:
        modelo = pickle.load(file)

    # Dropdowns para variables categóricas
    gender = st.selectbox('Género', ['Male', 'Female'])
    mtrans = st.selectbox('Medio de Transporte', ['Public_Transportation', 'Walking', 'Automobile', 'Motorbike', 'Bike'])
    family_history = st.selectbox('Historial Familiar de Obesidad', ['no', 'yes'])
    favc = st.selectbox('Consume Comida Alta en Calorías', ['no', 'yes'])
    smoke = st.selectbox('Fuma', ['no', 'yes'])
    scc = st.selectbox('Monitorea su Consumo de Calorías', ['no', 'yes'])
    caec = st.selectbox('Frecuencia de Consumo de Comida entre Comidas', ['no', 'Sometimes', 'Frequently', 'Always'])
    calc = st.selectbox('Frecuencia de Consumo de Alcohol', ['no', 'Sometimes', 'Frequently', 'Always'])

    # Campos numéricos
    age = st.number_input('Edad', min_value=0, max_value=100, step=1)
    fcvc = st.number_input('Consumo de Verduras (Frecuencia)', min_value=1.0, max_value=3.0, step=0.1)
    ncp = st.number_input('Número de Comidas Principales al Día', min_value=1.0, max_value=4.0, step=0.1)
    ch2o = st.number_input('Consumo de Agua al Día (Litros)', min_value=1.0, max_value=3.0, step=0.1)
    faf = st.number_input('Frecuencia de Actividad Física (Veces por Semana)', min_value=0.0, max_value=3.0, step=0.1)
    tue = st.number_input('Tiempo Usando Dispositivos Electrónicos (Horas)', min_value=0.0, max_value=2.0, step=0.1)

    # Generar columnas faltantes con valor 0
    input_data = {key: 0 for key in modelo.feature_names_in_}

    # Asignar los valores del usuario
    input_data.update({
        'Age': age,
        'FCVC': fcvc,
        'NCP': ncp,
        'CH2O': ch2o,
        'FAF': faf,
        'TUE': tue,
        'Gender_Male': 1 if gender == 'Male' else 0,
        f'MTRANS_{mtrans}': 1,
        'family_history': 1 if family_history == 'yes' else 0,
        'FAVC': 1 if favc == 'yes' else 0,
        'SMOKE': 1 if smoke == 'yes' else 0,
        'SCC': 1 if scc == 'yes' else 0,
        'CAEC': {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3}[caec],
        'CALC': {'no': 0, 'Sometimes': 1, 'Frequently': 2, 'Always': 3}[calc]
    })

    df_input = pd.DataFrame([input_data])

    # Botón para iniciar la predicción
    if st.button('Predecir Nivel de Obesidad'):
        prediccion = modelo.predict(df_input)
        niveles_obesidad = {
            0: 'Insufficient Weight',
            1: 'Normal Weight',
            2: 'Overweight Level I',
            3: 'Overweight Level II',
            4: 'Obesity Type I',
            5: 'Obesity Type II',
            6: 'Obesity Type III'
        }
        resultado = niveles_obesidad[prediccion[0]]
        st.success(f'El modelo predice: {resultado}')
with tab2:
    st.title('Visualización del Data Pipeline')

    # Imagen del Data Pipeline
    image_path = 'C:/Dev/Administración de Datos/Pipeline.jpg'
    image = Image.open(image_path)
    st.image(image, caption='Esquema del Data Pipeline', use_column_width=True)

    # Explicación de cada paso
    st.header('Paso 1: Verificación de usuario y autenticación')
    st.markdown('<p style="font-size: 18px;">El sistema solicita al usuario que ingrese su nombre y contraseña. Se verifica si el usuario está registrado y si la contraseña es correcta. Si no tiene permisos suficientes, se bloquea el acceso.</p>', unsafe_allow_html=True)

    st.header('Paso 2: Extracción de datos')
    st.markdown('<p style="font-size: 18px;">El sistema se conecta a Kaggle utilizando las credenciales almacenadas y descarga un conjunto de datos específico. Luego, extrae los datos descargados para poder trabajar con ellos.</p>', unsafe_allow_html=True)

    st.header('Paso 3: Encriptación y respaldo de datos')
    st.markdown('<p style="font-size: 18px;">Antes de realizar modificaciones, se genera una copia de seguridad de los datos originales. Para proteger la privacidad, los datos se encriptan y se almacenan en un archivo seguro.</p>', unsafe_allow_html=True)

    st.header('Paso 4: Procesamiento de los datos')
    st.markdown('<p style="font-size: 18px;">Los datos encriptados se desencriptan para poder ser utilizados en el modelo. Una vez desencriptados, se guardan temporalmente en un archivo accesible.</p>', unsafe_allow_html=True)

    st.header('Paso 5: Elaboración del modelo')
    st.markdown('<p style="font-size: 18px;">Se ejecuta automáticamente un notebook de Jupyter que entrena un modelo de machine learning utilizando los datos procesados. Al finalizar, el archivo desencriptado se elimina para garantizar la seguridad. Se verifica si el modelo se generó correctamente y si el archivo de resultados, modelo_final.pkl, está disponible.</p>', unsafe_allow_html=True)

    st.header('Paso 6: Almacenamiento en la nube')
    st.markdown('<p style="font-size: 18px;">Si el proceso se completa con éxito, el pipeline guarda los cambios en el código y los sube automáticamente a GitHub para mantener una copia actualizada.</p>', unsafe_allow_html=True)

    st.header('Procedimientos adicionales')
    st.markdown('<p style="font-size: 18px;">Se eliminan archivos temporales innecesarios, como modelo.nbconvert.ipynb, para mantener limpio el repositorio. Además, todas las acciones importantes se registran en un archivo de auditoría, audit_log.txt, para facilitar el seguimiento y la resolución de problemas.</p>', unsafe_allow_html=True)
