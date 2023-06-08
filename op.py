import streamlit as st
from streamlit import session_state

def main():

    st.sidebar.title("Escenarios")
    options = ['Escenario Nacional', 'Escenario Internacional', 'Resultados']
    if "choice" not in session_state:
        session_state.choice = "Escenario Nacional"
    choice = st.sidebar.selectbox("Selecciona una sección", options, options.index(session_state.choice))
    session_state.choice = choice

    if choice == "Escenario Nacional":
        mostrar_formulario_1()
    elif choice == "Escenario Internacional":
        mostrar_formulario_2()
    elif choice == "Resultados":
        resultados()
def resultados():
    pass

def mostrar_formulario_1():
    st.title("Formulario 1")
    if "formulario1" not in session_state:
        session_state.formulario1 = {
                                    "Cantidad":0.0,
                                    "Frecuencia":0.0,
                                    "Lead time planta-puerto":0.0,
                                    "Semanas cxp":0.0,
                                    "Moq":0.0,
                                    "Adu":0.0,
                                    "Factor lead time":0.0,
                                    "Factor variación":0.0,
                                    "Estandar posición":0.0,
                                    "Tarifa almacenamiento":0.0}
    
    Cantidad = st.number_input("Cantidad", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Cantidad"])
    Frecuencia = st.number_input("Frecuencia", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Frecuencia"])
    Lead_time_planta_puerto = st.number_input("Lead time planta-puerto", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Lead time planta-puerto"])
    Semanas_cxp = st.number_input("Semanas cxp", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Semanas cxp"])
    Moq = st.number_input("Moq", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Moq"])
    Adu = st.number_input("Adu", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Adu"])
    Factor_lead_time = st.number_input("Factor lead time",step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Factor lead time"])
    Factor_variación = st.number_input("Factor variación", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Factor variación"])
    Estandar_posición = st.number_input("Estandar posición", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Estandar posición"])
    Tarifa_almacenamiento = st.number_input("Tarifa almacenamiento", step=0.1, min_value=0.0, max_value=100000.0, value=session_state.formulario1["Tarifa almacenamiento"])


    if st.button("Enviar"):
        session_state.formulario1 = {
                                    "Cantidad":Cantidad,
                                    "Frecuencia":Frecuencia,
                                    "Lead time planta-puerto":Lead_time_planta_puerto,
                                    "Semanas cxp":Semanas_cxp,
                                    "Moq":Moq,
                                    "Adu":Adu,
                                    "Factor lead time":Factor_lead_time,
                                    "Factor variación":Factor_variación,
                                    "Estandar posición":Estandar_posición,
                                    "Tarifa almacenamiento":Tarifa_almacenamiento}
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
