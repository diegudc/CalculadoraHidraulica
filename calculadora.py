import streamlit as st
import pandas as pd
import numpy as np
import base64

he_turbina = 15.7
vol_deposito = 9000
t_turbinado = 1


# Estilos CSS personalizados
st.markdown("""
    <style>
    /* Cambiar el tamaño y color del título */
    .title {
        font-size: 36px !important;
        color: #000000;  /* Cambia el color a Negro */
        text-align: center;
    }
    
    /* Cambiar color del texto dentro del selectbox */
    .stSelectbox > div:first-child {
        color: #000000 !important; /* Cambia este color al que prefieras */
        font-size: 18px !important; /* Ajusta el tamaño del texto */
    }
            
    /* Cambiar el tamaño y color del texto del encabezado */
    .header {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        font-size: 28px !important;
        color: #000000;  /* Cambia el color a negro */
    }
    
    /* Cambiar el estilo de los campos de entrada (number_input, text_input) */
    input[type=number] {
        font-size: 20px;
        color: #FF6347;  /* Cambia el color del texto a rojo*/
        background-color: #FFF5EE;  /* Fondo crema claro */
        border: 2px solid #FF6347;  /* Borde en rojo*/
        padding: 5px;
        border-radius: 5px;
    }

    /* Específico para cambiar el tamaño de las etiquetas de number_input */
    div.stNumberInput > label {
        font-size: 30px;  /* Cambiar el tamaño de la etiqueta */
        font-weight: bold;  /* Cambiar el grosor de la fuente a negrita */
        color: #00000;  /* Cambiar el color de la etiqueta (rojo) */
        background-color: white;  /* Fondo blanco */
        padding: 3px;  /* Agregar un poco de espacio alrededor del texto */
        border-radius: 5px;  /* Bordes redondeados para el fondo blanco */
    }
            
    /* Cambiar el estilo de los botones */
    .stButton > button {
        font-size: 18px;
        color: white;
        background-color: #008CBA;  /* Azul */
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    /* Estilos para los botones alineados a los extremos */
    .button-container {
        display: flex;
        justify-content: space-between;  /* Alinea los botones a la izquierda y derecha */
        width: 100%;  /* Ocupa todo el ancho disponible */
        padding: 10px 0;  /* Añade un pequeño espacio entre los botones 
    }
           
    /* Estilos para la tabla con fondo blanco */
    .stDataFrame {
        font-size: 16px;
        color: #000000;  /* Color del texto */
        background-color: #FFFFFF !important;  /* Fondo blanco */
        border-radius: 5px;
        padding: 10px;
        border-collapse: collapse;
        width: 100%;
    }

    .stDataFrame table {
        width: 100%;
        border-collapse: collapse; /* Elimina los bordes de las celdas duplicados */
    }

    .stDataFrame th, .stDataFrame td {
        padding: 10px;
        border: 1px solid #ddd;  /* Bordes suaves */
        text-align: left;
    }

    .stDataFrame th {
        background-color: #f2f2f2;  /* Fondo gris claro para los encabezados */
    }

    /* Asegura que los bordes de la tabla sean visibles y consistentes */
    .stDataFrame td {
        background-color: #FFFFFF !important;  /* Aseguramos que el fondo de las celdas sea blanco */
    }
               
    </style>
    """, unsafe_allow_html=True)

# Función para cargar una imagen local y convertirla a Base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Función para cambiar el fondo de la página con una imagen
def set_background_image(image_path):
    # Cargar la imagen en Base64
    bin_str = get_base64_of_bin_file(image_path)
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/webp;base64,{bin_str}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Establecer el fondo de la aplicación con una imagen local
set_background_image('fondo.webp')  # Cambia esto por la ruta correcta a tu imagen

# Función para mostrar los resultados
def show_results_ej1(input1, input2, input3, input4, input5, input6 , input7, input8, input9):
    # Ejemplo de calculo, aquí lo que calcules depende de los inputs
    coef_potencia = input6 *input7*input8*input9
    E_generada = +coef_potencia*1000*9.806*(input1/1000)*(input2*10-input3)/3600
    E_bateria = input4*input5/1000
    cisternas_num = E_bateria / E_generada
    
    # Crear una tabla con resultados
    data = {
    "Coeficiente de potencia" : [coef_potencia],
    "Energia generada [Wh/lavado]" : [E_generada],
    "Energia bateria [Wh]" : [E_bateria],
    "Resultado nº de veces que hay usar la lavadora" : [cisternas_num]}
    
    df = pd.DataFrame(data)
    df = df.round(2)  # 2 decimales
    st.dataframe(df)

def show_results_ej2 (input1, input2, input3, input4, input5, input6 , input7, input8, he_turbina, vol_deposito, t_turbinado):
    vol = input2*input3
    hs_turbina = input4-he_turbina
    coef_potencia = input5 *input6*input7*input8
    q_turbinado = vol_deposito/1000/t_turbinado/3600
    P_turbina = coef_potencia*1000*9.806*q_turbinado*he_turbina
    E_electrica = coef_potencia*1000*9.806*he_turbina*vol_deposito/1000/3600
    Pluviometria_anual = input1*input3
    Depositos_anio = Pluviometria_anual/vol_deposito
    E_anual = Depositos_anio*E_electrica/1000
        # Crear una tabla con resultados
    data = {'Pluviometria anual [l]': [Pluviometria_anual],
    "Coeficiente de potencia" : [coef_potencia], 
    "Caudal turbinado [m^3/s]" : [q_turbinado],
    'Potencia turbinado en 1h [W]': [P_turbina], 
    "Energia generada por deposito  [Wh/deposito]" : [E_electrica],
    "Depositos al año" : [Depositos_anio],
    "Energia electrica anual [kWh/año]" : [E_anual]}
    df = pd.DataFrame(data)
    df = df.round(2)  # 2 decimales
    st.dataframe(df)

def show_results_ej3 (input1, input2, input3, input4, input5, input6 , input7, input8, he_turbina, vol_deposito, t_turbinado):
    vol = input2*input3
    hs_turbina = input4-he_turbina
    coef_potencia = input5 *input6*input7*input8
    q_turbinado = vol_deposito/1000/t_turbinado/3600
    P_turbina = coef_potencia*1000*9.806*q_turbinado*he_turbina
    E_electrica = coef_potencia*1000*9.806*he_turbina*vol_deposito/1000/3600
    Pluviometria_anual = input1*input3
    Depositos_anio = Pluviometria_anual/vol_deposito
    E_anual = Depositos_anio*E_electrica/1000
        # Crear una tabla con resultados
    data = {'Pluviometria anual [l]': [Pluviometria_anual],
    "Coeficiente de potencia" : [coef_potencia], 
    "Caudal turbinado [m^3/s]" : [q_turbinado],
    'Potencia turbinado en 1h [W]': [P_turbina], 
    "Energia generada por deposito  [Wh/deposito]" : [E_electrica],
    "Depositos al año" : [Depositos_anio],
    "Energia electrica anual [kWh/año]" : [E_anual]}
    df = pd.DataFrame(data)
    df = df.round(2)  # 2 decimales
    st.dataframe(df)
    


# Título de la aplicación
st.markdown('<h1 class="title">¿CÓMO USAR LA ENERGÍA HIDRÁULICA EN AMBITO URBANO?' , unsafe_allow_html=True)
# Estado de sesión para guardar el ejercicio seleccionado
if 'exercise_option' not in st.session_state:
    st.session_state.exercise_option = "Ejercicio 1"

# Menú de selección
option = st.selectbox("", ["Ejercicio 1", "Ejercicio 2", "Caso Particular" ], index=["Ejercicio 1", "Ejercicio 2", "Caso Particular"].index(st.session_state.exercise_option))

if option == "Ejercicio 1":
    st.markdown("""
        <div class="header">
        <h3>Ejercicio 1:</h3>
        <p>¿Cuántas ciclos de lavadora hay que usar para recargar la batería de un ordenador?</p>
        <p>Datos disponibles:</p>
        <ul>
            <li>Volumen de agua de la lavadora: 181 litros</li>
            <li>Presión del agua: 6 bar</li>
            <li>Altura de la lavadora sobre la cota 0: 2 metros</li>
            <li>Capacidad de la batería del Tesla Model S: 4400 mAh a 240 V</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    st.write("")
    # Crear los campos de entrada
    input1 = st.number_input("Volumen de la lavadora [l]", value = 181 )
    input2 = st.number_input("Presión de la acometida [bar]", value = 6)
    input3 = st.number_input("Altura de la lavadora [m]", value = 2)
    input4 = st.number_input("Capacidad de la batería [mAh]", value = 4400)
    input5 = st.number_input("Tensión de la batería [V]", value = 14.4)
    input6 = st.number_input("Rendimiento de la turbina", value = 0.9)
    input7 = st.number_input("Rendimiento del multiplicador", value = 0.9)
    input8 = st.number_input("Rendimiento de la generador", value = 0.85)
    input9 = st.number_input("Rendimiento del transformador", value = 0.9)
    
    # Estilo actualizado para los botones y la alineación
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # Botón de calcular resultado
    if st.button("Calcular resultado"):
        show_results_ej1(input1, input2, input3, input4, input5, input6 , input7, input8, input9)

    # Botón de ver otro ejercicio 
    if st.button("Ver otro ejercicio"):
        st.session_state.exercise_option = "Ejercicio 2"  # Cambiar la opción al segundo ejercicio  
    # Cerrar el contenedor de botones
    st.markdown('</div>', unsafe_allow_html=True)

elif option == "Ejercicio 2":
    st.markdown("""
        <div class="header">
        <h3>Ejercicio 2:</h3>
        <p>En la Universidad Pública de Oviedo (UniOvi), han copiado el sistema utilizado en el edificio 
        departamental para la captación de agua pluvial. Concretamente han puesto en marcha este proyecto en 
        el edificio de magisterio, situado en la  centro de la ciudad. Considerando que el sistema
        de aprovechamiento sigue los mismos criterios que en el edificio departamental de la universidad de La Rioja, 
        calcular la potencia de turbina necesaria, el volumen de depósito necesario y la energía se puede generar al año del 
        aprovechamiento de la energía pluvial. 
        Para ello, deberéis buscar información acerca de las precipitaciones medias que hay al año en Oviedo (1198.82 l/año)
        Otros datos<p>
        <ul>
            <li>La precipitación máxima la establecemos en 50 l/h·m2 </li>
            <li>La altura a la que se pone el depósito son 10 m.</li>
            <li>La superficie de captación de agua es de 450 m2 (la superficie de cubierta de magisterio).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    st.write("")
    # Crear los campos de entrada
    he_turbina = st.number_input("Altura de entrada de la turbina [m]", value = 9)
    vol_deposito = st.number_input("Volumen del depósito [l]", value = 1000)
    t_turbinado = st.number_input("Tiempo de turbinado [h]" , value = 1)
    input1 = st.number_input("Precipitación anual [l/m^2]", value = 1198.82 )
    input2 = st.number_input("Máxima precipitacion en 1h [l/m^2*h]", value = 50)
    input3 = st.number_input("Área cubierta [m^2]", value = 450)
    input4 = st.number_input("Altura edificio [m]", value = 15.5) 
    input5 = st.number_input("Rendimiento de la turbina", value = 0.9)
    input6 = st.number_input("Rendimiento del multiplicador", value = 0.9)
    input7 = st.number_input("Rendimiento de generador", value = 0.85)
    input8 = st.number_input("Rendimiento del transformador", value = 0.9)
    
     # Estilo actualizado para los botones y la alineación
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # Botón de calcular resultado
    if st.button("Calcular resultado"):
        show_results_ej2(input1, input2, input3, input4, input5, input6 , input7, input8, he_turbina, vol_deposito, t_turbinado)

    # Botón de ver otro ejercicio 
    if st.button("Ver otro ejercicio"):
        st.session_state.exercise_option = "Ejercicio 2"  # Cambiar la opción al segundo ejercicio
        
    # Cerrar el contenedor de botones
    st.markdown('</div>', unsafe_allow_html=True)

elif option == "Caso Particular":
    st.markdown("""
            <div class="header">
            <h3>Calcular tu propio caso de hidráulica mediante pluviometría:</h3>
            </div>
            """, unsafe_allow_html=True)
    st.write("")    
    # Crear los campos de entrada
    he_turbina = st.number_input("Altura de entrada de la turbina [m]", value = 9)
    vol_deposito = st.number_input("Volumen del depósito [l]", value = 1000)
    t_turbinado = st.number_input("Tiempo de turbinado [h]" , value = 1)
    input1 = st.number_input("Precipitación anual [l/m^2]", value = 1198.82 )
    input2 = st.number_input("Máxima precipitacion en 1h [l/m^2*h]", value = 50)
    input3 = st.number_input("Área cubierta [m^2]", value = 450)
    input4 = st.number_input("Altura edificio [m]", value = 15.5) 
    input5 = st.number_input("Rendimiento de la turbina", value = 0.9)
    input6 = st.number_input("Rendimiento del multiplicador", value = 0.9)
    input7 = st.number_input("Rendimiento de generador", value = 0.85)
    input8 = st.number_input("Rendimiento del transformador", value = 0.9)
    
    # Estilo actualizado para los botones y la alineación
    st.markdown('<div class="button-container">', unsafe_allow_html=True)

    # Botón de calcular resultado
    if st.button("Calcular resultado"):
        show_results_ej3(input1, input2, input3, input4, input5, input6 , input7, input8, he_turbina, vol_deposito, t_turbinado)

