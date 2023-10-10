import streamlit as st
from streamlit import session_state

def main ():    
    ''' 
    Inicializa las variables, propone escenarios, genera posibles combinaciones de datos
    invoca funciones de impresion de de datos y funciones que permiten la optimizacion de resultados
    '''
    Dicc_Variables = {
         0: {'Nombre': "Cantidad: unidades negociadas, independiente del periodo de tiempo establecido (unidad de medida determinada por el negociador)",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         1: {'Nombre': "Frecuencia: Tiempo estimado para recalcular o recibir el próximo envío",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         2: {'Nombre': "lead time entrega en planta: tiempo estimado para entregar en planta (si se consideran varias plantas, tomar el tiempo mayor)",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         3: {'Nombre': "condición de pago: tiempo en semanas estimado para pagar al proveedor el pedido actual",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         4: {'Nombre': "Cantidad mínima a pedir: Cantidad dada en unidad de medida determinada por el negociador",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         5: {'Nombre': "Consumo promedio Semanal: Cantidad dada en unidad de medida determinada por el negociador (la suma de consumos promedio de las plantas en análisis)",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         6: {'Nombre': "Factor lead time: De 0 a 1 qué tan volátil es el lead time, siendo 0 muy seguro y 1 completamente variable",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         7: {'Nombre': "Factor variación: De 0 a 1 qué tan volátil es el consumo, siendo 0 muy seguro y 1 completamente variable",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         8: {'Nombre': "Unidades por estiba: Cantidad dada en unidad de medida determinada por el negociador",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         9: {'Nombre': "Tarifa almacenamiento por cada unidad de medida determinada por el negociador",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         10: {'Nombre': "Tarifa almacenamiento por cada unidad de medida determinada por el negociador",
             'Tipo': "Obligatorio",
             'Esenario': "Actual",
             'Tipo_Dato': "int",
             'Valor': -1}
    }
    
    st.title('Nearshoring')
    col1_0, col1_1, col1_2 = st.columns(3)
    with col1_0:
        estados_checkboxes=[True for i  in Dicc_Variables.items()]
        for i, checkbox_value in enumerate(estados_checkboxes):
            checkbox_label = f"Checkbox {i + 1}"
            estados_checkboxes[i] = st.checkbox(checkbox_label, value=checkbox_value)
    with col1_1:
        session_state.Dicc_Variables = mostrar_valores(Dicc_Variables,estados_checkboxes)
        st.write(session_state.Dicc_Variables)
    with col1_2:
        session_state.Dicc_Variables2 = mostrar_valores(Dicc_Variables,estados_checkboxes, '2','Retador')
        st.write(session_state.Dicc_Variables2)

    st.write(session_state.Dicc_Variables2)
    st.write(session_state.Dicc_Variables)

def mostrar_valores(diccionario,estados_checkboxes, ind='', escenario='Actual'):
    st.write(escenario)
    valores_editados = []
    for key, value in diccionario.items():
        nombre = value['Nombre']
        valor = value['Valor']              
        if escenario==value['Esenario'] or 'todos'==value['Esenario']:        
            if estados_checkboxes[key]:
                valor = st.text_input(f'Nombre: {nombre} {ind}', valor,disabled=False)
            else:
                valor = st.text_input(f'Nombre: {nombre} {ind}', valor, disabled=True)
            valores_editados.append(valor)
    if st.button(f'Guardar Valores {ind} '):
        for key, value in diccionario.items():
            if estados_checkboxes[key]:
                diccionario[key]['Valor'] = valores_editados[key]
        st.success('Valores guardados con éxito.')
        return diccionario
    return {}


if __name__ == '__main__':
    main()