import streamlit as st
from streamlit import session_state

def main():

    nombres=(
        "Cantidad",
        "Frecuencia",
        "Lead time planta-puerto",
        "Semanas cxp",
        "Moq",
        "Adu",
        "Factor lead time",
        "Factor variación",
        "Estandar posición",
        "Tarifa almacenamiento")
    
    st.sidebar.title("Escenarios")
    options = ['Escenario Nacional', 'Escenario Internacional', 'Resultados']
    if "choice" not in session_state:
        session_state.choice = "Escenario Nacional"
    choice = st.sidebar.selectbox("Selecciona una sección", options, options.index(session_state.choice))
    session_state.choice = choice

    if choice == "Escenario Nacional":
        mostrar_formulario_1(nombres)
    elif choice == "Escenario Internacional":
        mostrar_formulario_2()
    elif choice == "Resultados":
        resultados()
def resultados():
    pass

def mostrar_formulario_1(nombres):
    st.title("Escenario nacional")
    if "formulario1" not in session_state:
        session_state.formulario1 = {nombre: 0.0 for nombre in nombres}
    
    col1_1, col1_2 = st.columns(2)
    valores=[]
#     for nombre in nombres:
#         valores.append(st.number_input(nombre, step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1[nombre]))
    with col1_1:
            for i in range(8):
                valores.append(st.number_input(nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1[nombres[i]]))
    with col1_2:
            for i in range(8, 10):
                valores.append(st.number_input(nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1[nombres[i]]))
                    
    if st.button("Enviar"):        
        session_state.formulario1 = {nombre: valores[index] for index, nombre in enumerate(nombres)}
        st.success("Formulario 1 enviado")

def mostrar_formulario_2():
    st.title("Formulario 2")
    if "formulario2" not in session_state:
        session_state.formulario2 = {"email": "", "telefono": ""}
    email = st.text_input("Email", session_state.formulario2["email"])
    telefono = st.text_input("Teléfono", session_state.formulario2["telefono"])
    if st.button("Enviar"):
        session_state.formulario2 = {"email": email, "telefono": telefono}
        st.success("Formulario 2 enviado")

def mostrar_formulario_3():
    st.title("Formulario 3")
    if "formulario3" not in session_state:
        session_state.formulario3 = {"pregunta": ""}
    pregunta = st.text_area("Pregunta", session_state.formulario3["pregunta"])
    if st.button("Enviar"):
        session_state.formulario3 = {"pregunta": pregunta}
        st.success("Formulario 3 enviado")

if __name__ == "__main__":
    main()
