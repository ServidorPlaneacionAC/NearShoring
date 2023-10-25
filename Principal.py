import streamlit as st
from streamlit import session_state
import copy
from pulp import *

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
         4: {'Nombre': "Inventario promedio: Inventario promedio del material",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         5: {'Nombre': "Consumo promedio Semanal: Cantidad dada en unidad de medida determinada por el negociador (la suma de consumos promedio de las plantas en análisis)",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         6: {'Nombre': "Tarifa gestion cargo: Cobro del material en gestion cargo",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         7: {'Nombre': "Costo transporte: Costo por unidad en el camion",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         8: {'Nombre': "Tarifa almacenamiento por cada unidad de medida determinada por el negociador",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         9: {'Nombre': "Tasa",
             'Tipo': "Obligatorio",
             'Esenario': "todos",
             'Tipo_Dato': "int",
             'Valor': -1},
         10: {'Nombre': "Precio a pagar",
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
        if "Dicc_Variables" not in session_state :            
            session_state.Dicc_Variables = (mostrar_valores(copy.deepcopy(Dicc_Variables),estados_checkboxes))       
        else:
            session_state.Dicc_Variables = (mostrar_valores(copy.deepcopy(session_state.Dicc_Variables),estados_checkboxes))       
    with col1_2:
        if "Dicc_Variables2" not in session_state :            
            session_state.Dicc_Variables2 = mostrar_valores(copy.deepcopy(Dicc_Variables),estados_checkboxes,'2','Retador')       
        else: 
            session_state.Dicc_Variables2 = mostrar_valores(copy.deepcopy(session_state.Dicc_Variables2),estados_checkboxes,'2','Retador')       



    if st.button(f'lucas'):
        valores_dicc_1 = organizar_campos(session_state.Dicc_Variables)
        valores_dicc_2 = organizar_campos(session_state.Dicc_Variables2)
        optimizacion(*valores_dicc_1, session_state.Dicc_Variables[10]["Valor"], *valores_dicc_2)
    


def organizar_campos(Diccionario): 
    '''
    Asigna los valores a los variables desde el diccionario
    '''
    cantidad = int(Diccionario[0]['Valor']) 
    frecuencia = int(Diccionario[1]['Valor'])
    lead_time=int(Diccionario[2]['Valor'])
    condicion_pago= int(Diccionario[3]['Valor'])
    inv_prom = int(Diccionario[4]['Valor'])
    asu = int(Diccionario[5]['Valor'])
    tarifa_gz = int(Diccionario[6]['Valor'])
    costo_transporte=int(Diccionario[7]['Valor'])
    tarifa_alm = int(Diccionario[8]['Valor'])
    tasa = int(Diccionario[9]['Valor'])

    return [cantidad,frecuencia,lead_time,condicion_pago,inv_prom,asu,tarifa_gz,costo_transporte,tarifa_alm,tasa]
 
def optimizacion(cantidad,frecuencia,lead_time,condicion_pago,inv_prom,asu,tarifa_gz,costo_transporte,tarifa_alm,tasa,precio,
                 cantidad_1,frecuencia_1,lead_time_1,condicion_pago_1,inv_prom_1,asu_1,tarifa_gz_1,costo_transporte_1,tarifa_alm_1,tasa_1):
    '''
    Me calcula los costos y me realiza la optimización
    '''
    # Creamos un objeto de problema de optimización llamado "prob" con objetivo de minimización
    # "Mi problema de optimización" es el nombre del problema, y LpMinimize indica que estamos minimizando
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    # Creamos una variable de optimización llamada "p_1" con límite inferior de 0
    # "p_1" es el nombre de la variable, y lowBound=0 establece el límite inferior en 0
    p_1 = LpVariable("p_1", lowBound=0)
    # Asignamos el valor de la variable de optimización "p_1" a la variable "precio_compra_1"
    precio_compra_1=p_1  
    inv_prom_sem_1 = inv_prom_1 / asu_1  # Inventario promedio por semana: Inventario promedio dividido por adu_1
    diferencial_1 = lead_time_1 - condicion_pago_1  # Diferencial: Tiempo de tránsito logístico menos semanas de crédito proveedor
    costo_inv_1 = precio_compra_1 * inv_prom_1  # Costo de inventario: Precio de compra por inventario promedio
    costo_nacionalizacion_1 = tarifa_gz_1 * cantidad_1 * precio_compra_1 # Costo de nacionalización: TAF GZ multiplicado por cantidad_1 y por el precio
    costo_cap_1 = (diferencial_1 + inv_prom_sem_1) * asu_1 * (((1 + tasa) ** (1/52)) - 1) * precio_compra_1  # Costo de capital: Cálculo con diferenciales, tasa, adu_1 y precio_compra_1
    costo_maninv_1 = (inv_prom_1) * (tarifa_alm_1 / 4.3) * (inv_prom_sem_1)  # Costo de manipulación de inventario: Producto de factores por inventario promedio semanal
    costo_compra_1 = precio_compra_1 * cantidad_1  # Costo de compra: Precio de compra por cantidad
    costo_total_1 = costo_maninv_1 + costo_compra_1 + costo_cap_1 + costo_transporte_1 + costo_nacionalizacion_1 # Costo total: Suma de varios costos
    costo_ebitda_1 = costo_total_1# Costo EBITDA: Suma de costos relevantes
    costo_unitario_1 = costo_total_1 / cantidad_1  # Costo unitario: Costo total dividido por cantidad
    capital_invertido_1 = ((diferencial_1 + inv_prom_sem_1) * (asu_1)) * (precio_compra_1)


    #calculos otro escenario
    inv_prom_sem = inv_prom / asu  # Inventario promedio por semana: Inventario promedio dividido por adu_1
    diferencial = lt - semanas_cxp  # Diferencial: Tiempo de tránsito logístico menos semanas de crédito proveedor
    costo_inv = precio_compra * inv_prom  # Costo de inventario: Precio de compra por inventario promedio
    costo_nacionalizacion = taf_gz * cantidad * precio_compra # Costo de nacionalización: TAF GZ multiplicado por cantidad_1 y por el precio
    costo_cap = (diferencial + inv_prom_sem) * adu * (((1 + tasa) ** (1/52)) - 1) * precio_compra  # Costo de capital: Cálculo con diferenciales, tasa, adu_1 y precio_compra_1
    costo_maninv = (inv_prom) * (tarifa_alm / 4.3) * (inv_prom_sem)  # Costo de manipulación de inventario: Producto de factores por inventario promedio semanal
    costo_compra = precio_compra * cantidad  # Costo de compra: Precio de compra por cantidad
    costo_total = costo_maninv + costo_compra + costo_cap + costo_transporte + costo_nacionalizacion # Costo total: Suma de varios costos
    costo_ebitda = costo_total# Costo EBITDA: Suma de costos relevantes
    costo_unitario = costo_total / cantidad  # Costo unitario: Costo total dividido por cantidad
    capital_invertido = ((diferencial + inv_prom_sem) * (adu)) * (precio_compra)

    #calculo variables financieras
    # Cálculo del EBITDA
    ebitda = costo_ebitda_1 - costo_ebitda
    # Cálculo de Impuestos
    impuestos = ebitda * 0.26
    # Cálculo de UODI (Utilidad Operativa Después de Impuestos)
    uodi = ebitda - impuestos
    # Cálculo del Diferencial de Capital Invertido
    diferencial_ct = capital_invertido - capital_invertido_1
    # Cálculo del Costo de Capital
    costo_capital = diferencial_ct * (((1 + tasa) ** (1 / 52)) - 1)
    # Cálculo de EVA (Valor Económico Agregado)
    eva = uodi - costo_capital


    # Define las variables de cambio de precio
    # Agrega restricciones
    prob += eva >= 0
    # Define la función objetivo
    prob += eva == 0
    status = prob.solve()

def mostrar_valores(diccionario,estados_checkboxes, ind='', escenario='Actual'):
    diccionario=copy.deepcopy(diccionario)
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

    for key, value in diccionario.items():
        if estados_checkboxes[key] and (escenario==value['Esenario'] or 'todos'==value['Esenario']):
            diccionario[key]['Valor'] = valores_editados[key]
    return diccionario
    

if __name__ == '__main__':
    main()
