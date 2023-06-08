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
    
    nombres_2=(
        "Cantidad",
        "Frecuencia",
        "Icoterm",   
        "lead time planta-puerto",
        "Semanas cxp",
        "Moq",
        "Adu",
        "Factor lead time",
        "Factor variación",
        "Estandar posición",
        "lead time tiempo-admon",
        "lead time puerto-puerto",
        "lead time gestión cargo",
        "lead time gz-planta",
        "Tarifa almacenamiento",
        "Precio compra")
    
    st.sidebar.title("Escenarios")
    options = ['Escenario Nacional', 'Escenario Internacional', 'Resultados']
    if "choice" not in session_state:
        session_state.choice = "Escenario Nacional"
    choice = st.sidebar.selectbox("Selecciona una sección", options, options.index(session_state.choice))
    session_state.choice = choice

    if choice == "Escenario Nacional":
        if "formulario1" not in session_state:
            session_state.formulario1 = mostrar_formulario_1(choice,nombres)
        else:
            session_state.formulario1 = mostrar_formulario_1(choice,nombres, session_state.formulario1)
    elif choice == "Escenario Internacional":
        if "formulario2" not in session_state:
            session_state.formulario2 = mostrar_formulario_1(choice,nombres_2)
        else:
            session_state.formulario2 = mostrar_formulario_1(choice,nombres_2, session_state.formulario2)
    elif choice == "Resultados":
        resultados()
        
def resultados():
    pass

def mostrar_formulario_1(titulo,nombres, formulario1=None):
    st.title(titulo)
    if formulario1 is None:
        formulario1 = {nombre: (0.0 if nombre!= "Icoterm" else "") for nombre in nombres}
    
    col1_1, col1_2 = st.columns(2)
    valores = []
    
    with col1_1:
        for i in range(int(len(nombres)/2)):
            if "Icoterm"==nombres[i]:
                valores.append(st.text_input(nombres[i], value=formulario1[nombres[i]]))
            else:    
                valores.append(st.number_input(nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))
    
    with col1_2:
        for i in range(int(len(nombres)/2), len(nombres)):
            valores.append(st.number_input(nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))
                    
    if st.button("Enviar"):        
        formulario1 = {nombre: valores[index] for index, nombre in enumerate(nombres)}
        st.success("Formulario 1 enviado")
    
    return formulario1

if __name__ == "__main__":
    main()
