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
        "Cantidad: unidades negociadas, independiente del periodo de tiempo establecido (unidad de medida determinada por el negociador)",
        "Frecuencia: Tiempo estimado para recalcular o recibir el próximo envío",
        "lead time: tiempo estimado para entregar en planta",
        "condición de pago: tiempo en semanas estimado para pagar alproveedor el pedido actual",
        "Consumo promedio Semanal: Cantidad dada en unidad de medida determinada por el negociador (la suma de consumos promedio de las plantas en análisis)",
        "Inventario promedio:",
        "Tarifa gestion cargo:",
        "Costo de transporte: Costo por unidad en un camion",
        "Tarifa almacenamiento por cada unidad de medida determinada por el negociador",
        "Factor de importacion")
    
    nombres_2=(        
        "Cantidad: unidades negociadas, independiente del periodo de tiempo establecido (unidad de medida determinada por el negociador)",
        "Frecuencia: Tiempo estimado para recalcular o recibir el próximo envío",
        "lead time: tiempo estimado para entregar en planta",
        "condición de pago: tiempo en semanas estimado para pagar alproveedor el pedido actual",
        "Consumo promedio Semanal: Cantidad dada en unidad de medida determinada por el negociador (la suma de consumos promedio de las plantas en análisis)",
        "Inventario promedio:",
        "Tarifa gestion cargo:",
        "Costo de transporte: Costo por unidad en un camion",
        "Tarifa almacenamiento por cada unidad de medida determinada por el negociador",
        "Flete internacional: por cada unidad de medida determinada por el negociador",
        "Arancel: por cada unidad de medida determinada por el negociador",
        "Costo por servir: por cada unidad de medida determinada por el negociador",
        "Flete nacional: por cada unidad de medida determinada por el negociador",
        "Factor de importacion",
        "Precio compra: no incluye aranceles")
    #el precio de compra = los 4 valores anteriores a el
    
    st.sidebar.title("Escenarios")
    options = ['Nuevo Escenario', 'Escenario Anterior', 'Resultados']
    if "choice" not in session_state:
        session_state.choice = "Nuevo Escenario"
    choice = st.sidebar.selectbox("Selecciona una sección", options, options.index(session_state.choice))
    session_state.choice = choice
    
    agregar_costo_capital = False
    agregar_costo_capital=st.sidebar.checkbox("Costo capital", value=agregar_costo_capital)  
    #Si se tiene en cuenta el costo capital se optimiza sobre el eva, sino obre el uodi
    esc_retador ="Escenario Nacional"
    opciones = ['Escenario Nacional', 'Escenario Internacional']
    if "esc_retador" not in session_state:
        session_state.esc_retador = "Escenario Nacional"
    frm= streamlit_frm(session_state.valor_en_pesos,session_state.trm)
    if choice == "Nuevo Escenario":
        session_state.esc_retador = st.selectbox("Selecciona si el escenario es nacional o internacional", opciones,opciones.index(session_state.esc_retador))
        if "Escenario Nacional" == session_state.esc_retador:

            if "formulario1" not in session_state:
                session_state.formulario1,session_state.valor_en_pesos,session_state.error,session_state.trm = frm.mostrar_formulario_1(choice,nombres)
            else:
                session_state.formulario1,session_state.valor_en_pesos,session_state.error,session_state.trm = frm.mostrar_formulario_1(choice,nombres, session_state.formulario1)
        else:
            
            if "formulario3" not in session_state:
                session_state.formulario3,session_state.valor_en_pesos,session_state.error,session_state.trm = frm.mostrar_formulario_1(choice,nombres_2[:-6],transaccion_internacional=True)
            else:
                session_state.formulario3,session_state.valor_en_pesos,session_state.error,session_state.trm = frm.mostrar_formulario_1(choice,nombres_2[:-6], session_state.formulario3,transaccion_internacional=True)    
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
            #Se crean listar valores y valores_2, pues son los parametros que se recibe desde utils
            #como en los escenarios internacionales el precio es una variable que se compone de otras
            #variables el ciclo se parte hasta los ultimos 5 elementos, para que el último campo sea la 
            #suma de estos
            valores=[]
            valores_2=[]
            resultado=[]
            frm.tasa=st.sidebar.number_input("Tasa costo capital", step=0.01, min_value=0.0, max_value=2.0, value=0.12)
            for nombre in nombres_2[:-6]: #se parte el ciclo como se menciono antes
                valores_2.append(session_state.formulario2[nombre])
            valores_2.append(session_state.formulario2["Precio compra: no incluye aranceles"])
            for nombre in nombres_2[-6:-2]: #se suman todos los valores al ultimo
                valores_2[-1]+=(session_state.formulario2[nombre])
            valores_2[-1]=valores_2[-1]*session_state.formulario2["Factor de importacion"]
            #Almaceno valores en listas para pasarolo como parametros a las funciones eva y uodi 
            #Genero ciclos para crear tabla de valor y mostrar valores cercanos, los guardo en una matriz de 2 x 2 
            # la envío al metodo resultados
            if session_state.esc_retador == "Escenario Nacional":
                for nombre in nombres[:]:
                    valores.append(session_state.formulario1[nombre])
                if agregar_costo_capital:   
                    resultado.append(calculos.eva(valores,valores_2,frm.tasa))
                    for i in range(-5,6,1):
                        resultado.append(calculos.valores_eva(valores,valores_2,resultado[0][0]+(i*(resultado[0][0]/15)),frm.tasa))
                else:
                    resultado.append(calculos.uodi(valores,valores_2,frm.tasa))
                    for i in range(-5,6,1):
                        resultado.append(calculos.valores_uodi(valores,valores_2,resultado[0][0]+(i*(resultado[0][0]/15)),frm.tasa))
            else:
                for nombre in nombres_2[:-6]:
                    valores.append(session_state.formulario3[nombre])
                if agregar_costo_capital:
                    
                    resultado.append(calculos.eva_int(valores,valores_2,frm.tasa))
                    for i in range(-5,6,1):
                        resultado.append(calculos.valores_eva_int(valores,valores_2,resultado[0][0]+(i*(resultado[0][0]/15)),frm.tasa))
                else:
                    
                    st.write('valores')    
                    st.write(valores)    
                    st.write('valores_2')    
                    st.write(valores_2)         
                    resultado.append(calculos.uodi_int(valores,valores_2,frm.tasa))
                    for i in range(-5,6,1):
                       resultado.append(calculos.valores_uodi_int(valores,valores_2,resultado[0][0]+(i*(resultado[0][0]/15)),frm.tasa))
            
            
            
            
            
                  
            frm.resultados(resultado,valores,valores_2,agregar_costo_capital,session_state.esc_retador)

if __name__ == "__main__":
    main()
