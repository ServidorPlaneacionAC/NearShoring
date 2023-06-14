import streamlit as st
from streamlit import session_state
from pulp import *
from streamlit_frm import streamlit_frm
import utils as calculos

def main():
    if "error" not in session_state:
        #Variable generada para validaciones, inicia en True porque al iniciar todos los datos estan sin diligenciar
        #si se diligencian y quedan con valores lógicos se apaga y permite guardar la informacion en las variables estados de sesion
        session_state.error=True
    if "trm" not in session_state:
        #Variable para almacenar la trm en los cambios de formularios
        session_state.trm=4800.00
    if "valor_en_pesos" not in session_state:
        #Variable para almacenar el valor_en_pesos en los cambios de formularios
        session_state.valor_en_pesos=00.00
      
    nombres=(
        "Cantidad: unidades con los que se generará la comparación entre proveedores",
        "Frecuencia: Temporalidad estimadda para recalcular próximo envío",
        "Lead time planta-puerto",
        "Semanas cxp: tiempo en semanas estimado para pagar a mi proveedor el pedido actual",
        "Moq: Cantidad mínima a pedir (en la unidad que se desee manejar)",
        "Adu: Consumo promedio diario (en la unidad que se desee manejar)",
        "Factor lead time: De 0 a 1 qué tan confiable es el lead time, siendo 0 muy seguro y 1 completamente variable",
        "Factor variación: De 0 a 1 qué tan confiable es el consumo, siendo 0 muy seguro y 1 completamente variable",
        "Estandar posición: Unidades por estiba",
        "Tarifa almacenamiento por unidad de consumo")
    
    nombres_2=(
        "Cantidad: unidades con los que se generará la comparación entre proveedores",
        "Frecuencia: Temporalidad estimadda para recalcular próximo enví",
        "Incoterm",   
        "lead time planta-puerto",
        "Semanas cxp: tiempo en semanas estimado para pagar a mi proveedor el pedido actual",
        "Moq: Cantidad mínima a pedir (en la unidad que se desee manejar)",
        "Adu: Consumo promedio diario (en la unidad que se desee manejar)",
        "Factor lead time: De 0 a 1 qué tan confiable es el lead time, siendo 0 muy seguro y 1 completamente variable",
        "Factor variación: De 0 a 1 qué tan confiable es el consumo, siendo 0 muy seguro y 1 completamente variable",
        "Estandar posición: Unidades por estiba",
        "lead time tiempo-admon",
        "lead time puerto-puerto",
        "lead time gestión cargo",
        "lead time gz-planta",
        "Tarifa almacenamiento por unidad de consumo",
        "Precio compra: no incluye aranceles")
    
    st.sidebar.title("Escenarios")
    options = ['Nuevo Escenario', 'Escenario Anterior', 'Resultados']
    if "choice" not in session_state:
        session_state.choice = "Nuevo Escenario"
    choice = st.sidebar.selectbox("Selecciona una sección", options, options.index(session_state.choice))
    session_state.choice = choice
    
    agregar_costo_capital = False
    agregar_costo_capital=st.sidebar.checkbox("Costo capital", value=agregar_costo_capital)  
    #Si se tiene en cuenta el costo capital se optimiza sobre el eva, sino obre el uodi
    
    frm= streamlit_frm(session_state.valor_en_pesos,session_state.trm)
    if choice == "Nuevo Escenario":
        if "formulario1" not in session_state:
            session_state.formulario1,session_state.valor_en_pesos,session_state.error,session_state.trm = frm.mostrar_formulario_1(choice,nombres)
        else:
            session_state.formulario1,session_state.valor_en_pesos,session_state.error,session_state.trm = frm.mostrar_formulario_1(choice,nombres, session_state.formulario1)
    elif choice == "Escenario Anterior":
        if "formulario2" not in session_state:
            session_state.formulario2,session_state.valor_en_pesos,session_state.error,session_state.trm = frm.mostrar_formulario_1(choice,nombres_2,transaccion_internacional=True)
        else:
            session_state.formulario2,session_state.valor_en_pesos,session_state.error,session_state.trm = frm.mostrar_formulario_1(choice,nombres_2, session_state.formulario2,transaccion_internacional=True)
    elif choice == "Resultados": 
        
         if "formulario2" not in session_state or "formulario1" not in session_state or session_state.error:
            #las variables de estado formulario 1 y 2 solo se inicializan si se toman como esta alternaativa en el menu de navegacion
            #Falta corregir que pasa si diligencio un formulario bien, entro al otro y no guardo
            st.error("no se ha diligenciado algun escenario")
         else:
            valores=[]
            valores_2=[]
            resultado=[]
            for nombre in nombres:
                valores.append(session_state.formulario1[nombre])
            for nombre in nombres_2:
                valores_2.append(session_state.formulario2[nombre])
            #Almaceno valores en listas para pasarolo como parametros a las funciones eva y uodi 
            if agregar_costo_capital:
                resultado.append(calculos.eva(valores,valores_2))
                for i in range(-5,6,1):
                    resultado.append(calculos.valores_eva(valores,valores_2,resultado[0][0]+(i*(resultado[0][0]/15))))
            else:
                resultado.append(calculos.uodi(valores,valores_2))
                for i in range(-5,6,1):
                    resultado.append(calculos.valores_uodi(valores,valores_2,resultado[0][0]+(i*(resultado[0][0]/15))))  
            frm.resultados(resultado)

if __name__ == "__main__":
    main()
