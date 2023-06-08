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
    
    agregar_costo_capital = False
    agregar_costo_capital=st.sidebar.checkbox("Costo capital", value=agregar_costo_capital)  
    
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
#         if agregar_costo_capital:
#             resultado = eva([session_state.formulario1[nombres[i]] for i in range(len(nombres))],
#                             [session_state.formulario1[nombres_2[j]] for j in range(len(nombres_2))])
#         else:
#             resultado = uodi([session_state.formulario1[nombres[i]] for i in range(len(nombres))],
#                              [session_state.formulario1[nombres_2[j]] for j in range(len(nombres_2))])
#         resultados(resultado)
        eva(nombres_2)
  
def eva(nombres):
    for nombre in nombres:
        st.write(session_state.formulario2[nombre])
    st.write("eva")
    
def uodi(valores,valores_2):
    st.tittle("uodi")
    
def resultados(resultado):
    st.write(f"El precio maximo a pagar es: {resultado[0]}")
    st.write(f"UODI: {resultado[1]}")
    st.write(f"EBITDA: {resultado[2]}")
    st.write(f"EVA: {resultado[3]}")
    st.write(f"ROIC: {0 if resultado[4] == 0 else resultado[1]/resultado[4]}")

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
