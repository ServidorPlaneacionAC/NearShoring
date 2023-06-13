import streamlit as st
from streamlit import session_state
from pulp import *
from streamlit_frm import streamlit_frm

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
        "Tarifa almacenamiento")
    
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
        "Tarifa almacenamiento",
        "Precio compra: no incluye aranceles")
    
    st.sidebar.title("Escenarios")
    options = ['Escenario Nacional', 'Escenario Internacional', 'Resultados']
    if "choice" not in session_state:
        session_state.choice = "Escenario Nacional"
    choice = st.sidebar.selectbox("Selecciona una sección", options, options.index(session_state.choice))
    session_state.choice = choice
    
    agregar_costo_capital = False
    agregar_costo_capital=st.sidebar.checkbox("Costo capital", value=agregar_costo_capital)  
    #Si se tiene en cuenta el costo capital se optimiza sobre el eva, sino obre el uodi
    
    frm= streamlit_frm(session_state.valor_en_pesos)
    if choice == "Escenario Nacional":
        if "formulario1" not in session_state:
            session_state.formulario1,session_state.valor_en_pesos,session_state.error = frm.mostrar_formulario_1(choice,nombres)
        else:
            session_state.formulario1,session_state.valor_en_pesos,session_state.error = frm.mostrar_formulario_1(choice,nombres, session_state.formulario1)
    elif choice == "Escenario Internacional":
        if "formulario2" not in session_state:
            session_state.formulario2,session_state.valor_en_pesos,session_state.error = frm.mostrar_formulario_1(choice,nombres_2,transaccion_internacional=True)
        else:
            session_state.formulario2,session_state.valor_en_pesos,session_state.error = frm.mostrar_formulario_1(choice,nombres_2, session_state.formulario2,transaccion_internacional=True)
    elif choice == "Resultados": 
        
        if "formulario2" not in session_state or "formulario1" not in session_state or session_state.error:
            #las variables de estado formulario 1 y 2 solo se inicializan si se toman como esta alternaativa en el menu de navegacion
            #Falta corregir que pasa si diligencio un formulario bien, entro al otro y no guardo
            st.error("no se ha diligenciado algun escenario")
        else:
            valores=[]
            valores_2=[]
            for nombre in nombres:
                valores.append(session_state.formulario1[nombre])
            for nombre in nombres_2:
                valores_2.append(session_state.formulario2[nombre])
            #Almaceno valores en listas para pasarolo como parametros a las funciones eva y uodi 
            if agregar_costo_capital:
                frm.resultado = eva(valores,valores_2)
            else:
                frm.resultado = uodi(valores,valores_2)
            resultados(resultado)
  

# def resultados(resultado):
#     st.write(f"El precio maximo a pagar es: {resultado[0]}")
#     st.write(f"UODI: {resultado[1]}")
#     st.write(f"EBITDA: {resultado[2]}")
#     st.write(f"EVA: {resultado[3]}")
#     st.write(f"ROIC: {0 if resultado[4] == 0 else resultado[1]/resultado[4]}")

# def mostrar_formulario_1(titulo,nombres, formulario1=None, transaccion_internacional=False):
#     '''Funcion que genera los formularios para evaluar las oportunidades de inversión, recibe nombre del escenario, lista nombres que
#         indica los campos del formulario, formulario1 que es un diccionario que donde se almacena los valores de los campos, si no se pasa por 
#         parametro inicializa las variables en 0 y transaccion_internacional que es un booleano que indica si se debe o no añadir la opción de 
#         indicar el precio en pesos y trasnformarlo'''
    
#     #inicializo variables locales para uso posterior
#     costo_dolares=0.0
#     checkbox_operacion_dolarizado=False
#     st.title(titulo)
#     if formulario1 is None:
#         #inicializo los valores en 0.0 o vacios si formulario1 no esta declarado
#         formulario1 = {nombre: (0.0 if nombre!= "Incoterm" else "") for nombre in nombres}
    
#     #indico que mostrare la informacion en 2 columnas e inicializo variable local valores que es donde voy a guardadr temporalmente las respuestas
#     col1_1, col1_2 = st.columns(2)
#     valores = []
    
#     with col1_1:
#         for i in range(int(len(nombres)/2)):
#             if "Incoterm"==nombres[i]:
#                 valores.append(st.text_input(nombres[i], value=formulario1[nombres[i]]))
#             else:    
#                 valores.append(st.number_input(nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))
        
#         if transaccion_internacional==True:
#             #genero proceso extra para transformar de dolares a pesos y pesos a dolares
#             checkbox_operacion_dolarizado = st.checkbox("indicar el precio en dolares")
#             if checkbox_operacion_dolarizado:
# #                 si se selecciono el checkbox_operacion_dolarizado entonces ingresa y hace la variable 
# #                     costo_dolares=session_state.valor_en_pesos(inicializada en el main con valor 0.0)/session_state.trm(inicializada en el main con valor 4.800) 
# #                     luego genero un campo para indicar trm al momento de la negociación, igual que el campo para indicar el precio en dolares,
# #                     luego hago guardo en la variable de estado valor_en_pesos el valor en pesos de la transaccion indicada
                    
#                 costo_dolares=session_state.valor_en_pesos/session_state.trm
#                 session_state.trm=st.number_input("Valor TRM", step=0.1000, min_value=0.0, max_value=100000.0, value=session_state.trm) 
#                 costo_dolares=st.number_input("Precio compra en dolares", step=0.001, min_value=0.0, max_value=100000.0, value=costo_dolares) 
#                 session_state.valor_en_pesos=costo_dolares*session_state.trm  
    
#     with col1_2:
# #         '''Si la transaccion no es dolarizada se traen todos los campos del formulario y ya'''
#         if transaccion_internacional==True:
#             for i in range(int(len(nombres)/2), len(nombres)-1):
#                 valores.append(st.number_input(nombres[i],key=nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))
#             if not checkbox_operacion_dolarizado:
# #                 Si no se ha seleccionado la alternativa de operacion dolarizda indico que el valor de la ultima variable puesta en nombre es lo que esta
# #                     en la variable de estado valor_en_pesos(inicializada en el main con valor 0.0 y modificada cuando selecciono la operacion dolarizada
# #                     y llevo a valor_en_pesos el valor que se escriba en este campo)
#                 valores.append(st.number_input(nombres[-1],key=nombres[-1], step=0.1, min_value=0.0, max_value=10000000.0, value=session_state.valor_en_pesos))
#                 session_state.valor_en_pesos=valores[-1]
#             else:            
#                 #traigo valor_en_pesos pero no permito su edicion
#                 valores.append(st.number_input(nombres[-1],key=nombres[-1], step=0.1, min_value=0.0, max_value=10000000.0, value=session_state.valor_en_pesos,disabled=True))
#         else:
#             for i in range(int(len(nombres)/2), len(nombres)):
#                 valores.append(st.number_input(nombres[i],key=nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))
                 
#     if st.button("Guardar"): 
#         if 0.0 in valores or "" in valores:
#             session_state.error=True
#             st.error("hay un dato con valor 0.0 o vacio")
#         else:
#             if transaccion_internacional==True:
#                 valores[-1]=session_state.valor_en_pesos
#             formulario1 = {nombre: valores[index] for index, nombre in enumerate(nombres)}
#             session_state.error=False
#             st.success("Datos guardados correctamente")
    
#     return formulario1

def eva(valores,valores_2):
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    p_1 = LpVariable("p_1", lowBound=0)
    precio_compra_1=p_1
    cantidad_1=valores[0]
    frecuencia_1=valores[1]
    lt_plantapuerto_1=valores[2]
    semanas_cxp_1=valores[3]
    moq_1=valores[4]
    adu_1=valores[5]
    factor_lt_1=valores[6]
    factor_var_1=valores[7]
    estandar_pos_1=valores[8]
    tarifa_alm_1=valores[9]


    #campos_1 calculados

    lt_completo_1=lt_plantapuerto_1
    lt_logistico_1=lt_plantapuerto_1
    zona_amarilla_1=lt_plantapuerto_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_plantapuerto_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_logistico_1-semanas_cxp_1

    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=0
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+0.12)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1
    costo_unitario_1=costo_total_1/cantidad_1
    capital_invertido_1=((diferencial_1+inv_prom_sem_1)*(adu_1))*(precio_compra_1)

    cantidad=valores_2[0]
    frecuencia=valores_2[1]
    icoterm = valores_2[2]
    lt_plantapuerto=valores_2[3]
    semanas_cxp=valores_2[4]
    moq=valores_2[5]
    adu=valores_2[6]
    factor_lt=valores_2[7]
    factor_var=valores_2[8]
    estandar_pos=valores_2[9]
    lt_tiempoadmon=valores_2[10]
    lt_puertopuerto=valores_2[11]
    lt_gz=valores_2[12]
    lt_gzplanta=valores_2[13]
    tarifa_alm=valores_2[14]
    precio_compra=valores_2[15]
    #campos calculados

    lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    lt_logistico= icoterm  
    if icoterm == "EXWORK":
        lt_logistico = lt_plantapuerto+lt_puertopuerto+lt_gzplanta+lt_gz
    elif icoterm == "FOB":
        lt_logistico = lt_puertopuerto+lt_gzplanta+lt_gz
    else:
        lt_logistico = lt_gzplanta+lt_gz
    zona_amarilla=lt_plantapuerto*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_plantapuerto*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_logistico-semanas_cxp
    taf_gz=0.07*precio_compra

    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=200*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+0.12)**(1/52))-1)*precio_compra
    costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    costo_compra=precio_compra*cantidad
    costo_total=costo_maninv+costo_compra+costo_cap+costo_nacionalizacion+costo_transportegz_planta
    costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    costo_unitario_0=costo_total/cantidad
    capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)


    #calculo variables financieras

    ebitda=costo_ebitda_1-costo_ebitda
    impuestos=ebitda*0.26
    uodi=ebitda-impuestos
    diferencial_ct=capital_invertido-capital_invertido_1
    costo_capital=(diferencial_ct)*(((1+0.12)**(1/52))-1)
    eva=uodi-costo_capital
    #roic=uodi/diferencial_ct

    c_0 = costo_unitario_0  # Costo del producto 0
    c_1 = costo_unitario_1  # Costo del producto 1
    p_0= precio_compra
    # Define las variables de cambio de precio
    #p_0 = LpVariable("p_0", lowBound=0)


    # Agrega restricciones
    #prob += p_0 <= 1
    #prob += p_1 <= 1
    #prob += p_0 >= 0
    prob += eva >= 0

    # Define la función objetivo
    #prob += c_1 - c_0 == p_1 - p_0 # Minimiza la diferencia de costos totales
    prob += eva == 0
    status = prob.solve()
#     return (p_1.value())
    return [p_1.value(),value(uodi),value(ebitda),value(eva),value(diferencial_ct)]
# nombres
    
def uodi(valores,valores_2):
    # Aquí va tu método m
    # Crear problema de minimización
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    p_1 = LpVariable("p_1", lowBound=0)
    precio_compra_1=p_1
    cantidad_1=valores[0]
    frecuencia_1=valores[1]
    lt_plantapuerto_1=valores[2]
    semanas_cxp_1=valores[3]
    moq_1=valores[4]
    adu_1=valores[5]
    factor_lt_1=valores[6]
    factor_var_1=valores[7]
    estandar_pos_1=valores[8]
    tarifa_alm_1=valores[9]
    
    #campos_1 calculados
    
    lt_completo_1=lt_plantapuerto_1
    lt_logistico_1=lt_plantapuerto_1
    zona_amarilla_1=lt_plantapuerto_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_plantapuerto_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_logistico_1-semanas_cxp_1
    
    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=0
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+0.12)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1
    costo_unitario_1=costo_total_1/cantidad_1
    capital_invertido_1=((diferencial_1+inv_prom_sem_1)*(adu_1))*(precio_compra_1)
    
    cantidad=valores_2[0]
    frecuencia=valores_2[1]
    icoterm = valores_2[2]
    lt_plantapuerto=valores_2[3]
    semanas_cxp=valores_2[4]
    moq=valores_2[5]
    adu=valores_2[6]
    factor_lt=valores_2[7]
    factor_var=valores_2[8]
    estandar_pos=valores_2[9]
    lt_tiempoadmon=valores_2[10]
    lt_puertopuerto=valores_2[11]
    lt_gz=valores_2[12]
    lt_gzplanta=valores_2[13]
    tarifa_alm=valores_2[14]
    precio_compra=valores_2[15]
    #campos calculados
    
    lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    lt_logistico= icoterm  
    if icoterm == "EXWORK":
        lt_logistico = lt_plantapuerto+lt_puertopuerto+lt_gzplanta+lt_gz
    elif icoterm == "FOB":
        lt_logistico = lt_puertopuerto+lt_gzplanta+lt_gz
    else:
        lt_logistico = lt_gzplanta+lt_gz
    zona_amarilla=lt_plantapuerto*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_plantapuerto*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_logistico-semanas_cxp
    taf_gz=0.07*precio_compra
    
    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=200*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+0.12)**(1/52))-1)*precio_compra
    costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    costo_compra=precio_compra*cantidad
    costo_total=costo_maninv+costo_compra+costo_cap+costo_nacionalizacion+costo_transportegz_planta
    costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    costo_unitario_0=costo_total/cantidad
    capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)


    #calculo variables financieras

    ebitda=costo_ebitda_1-costo_ebitda
    impuestos=ebitda*0.26
    uodi=ebitda-impuestos
    diferencial_ct=capital_invertido-capital_invertido_1
    costo_capital=(diferencial_ct)*(((1+0.12)**(1/52))-1)
    eva=uodi-costo_capital
    #roic=uodi/diferencial_ct
    c_0 = costo_unitario_0  # Costo del producto 0
    c_1 = costo_unitario_1  # Costo del producto 1
    p_0= precio_compra
    # Define las variables de cambio de precio
    #p_0 = LpVariable("p_0", lowBound=0)
    # Agrega restricciones
    #prob += p_0 <= 1
    #prob += p_1 <= 1
    #prob += p_0 >= 0
    prob += uodi >= 0
    # Define la función objetivo
    #prob += c_1 - c_0 == p_1 - p_0 # Minimiza la diferencia de costos totales
    prob += uodi == 0
    status = prob.solve()
#     return (p_1.value())
    return [p_1.value(),value(uodi),value(ebitda),value(eva),value(diferencial_ct)]

if __name__ == "__main__":
    main()
