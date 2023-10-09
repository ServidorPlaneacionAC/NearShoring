import streamlit as st

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
             'Valor': -1}
    }
    valores_editados,estados_checkboxes = mostrar_valores(Dicc_Variables)

    if st.button('Guardar Valores'):
        # Imprimir los valores editados en el diccionario
        for key, value in enumerate(Dicc_Variables):
            if estados_checkboxes[key]:
                Dicc_Variables[value]['Valor'] = valores_editados[key]
        st.success('Valores guardados con éxito.')
        mostrar_valores(Dicc_Variables)

def mostrar_valores(diccionario):
    st.title('Editar Valores')

    # Crear una lista para almacenar los valores editados y los estados de los checkboxes
    valores_editados = []
    estados_checkboxes = []

    # Iterar a través del diccionario y mostrar campos de entrada de texto y checkboxes para editar los valores
    for key, value in diccionario.items():
        nombre = value['Nombre']
        valor = value['Valor']
        editar_valor = st.checkbox(key)

        if editar_valor:
            valor = st.text_input(f'Nombre: {nombre}', valor,disabled=True)
        else:
            valor = st.text_input(f'Nombre: {nombre}', valor,disabled=False)

        valores_editados.append(valor)
        estados_checkboxes.append(editar_valor)
    return valores_editados,estados_checkboxes


if __name__ == '__main__':
    main()