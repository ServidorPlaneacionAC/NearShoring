import streamlit as st
from pulp import *



def main():

    escenario1=[]
    escenario2=[]
    agregar_costo_capital = False 
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
    valores = []
    valores_2 = []   
    resultado=[]

    agregar_costo_capital=st.sidebar.checkbox("Costo capital", value=agregar_costo_capital)  
    st.title("Nearshoring")
    st.sidebar.title("Escenarios")
    opciones = ['Escenario Nacional', 'Escenario Internacional', 'Resultados']

    # Renderizar los botones
    for opcion in opciones:
        if st.sidebar.button(opcion):
            if opcion == 'Escenario Nacional':
                esenario_nacional()
            elif opcion == 'Escenario Internacional':
                esenario_internacional()
            elif opcion == 'Resultados':
                resultados(resultado)

    
    if st.sidebar.button("Ejecutar método"):
        if agregar_costo_capital:
            resultado=resultados(eva(valores,valores_2))
        else:
            resultado=resultados(uodi(valores,valores_2))
            
def resultados(resultado):

    st.write(f"El precio maximo a pagar es: {resultado[0]}")
    st.write(f"UODI: {resultado[1]}")
    st.write(f"EBITDA: {resultado[2]}")
    st.write(f"EVA: {resultado[3]}")
    st.write(f"ROIC: {0 if resultado[4] == 0 else resultado[1]/resultado[4]}")    
    return=resultado
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

def eva(valores,valores_2):
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
    prob += eva >= 0

    # Define la función objetivo
    #prob += c_1 - c_0 == p_1 - p_0 # Minimiza la diferencia de costos totales
    prob += eva == 0
    status = prob.solve()
#     return (p_1.value())
    return [p_1.value(),value(uodi),value(ebitda),value(eva),value(diferencial_ct)]
# nombres

#st.sidebar.title("Escenarios")
#st.sidebar.button("Escenario nacional")
#st.sidebar.button("Escenario internacional")

# Definir la disposición en dos columnas
# col1, col2 = st.columns(2)
def esenario_nacional():
    # col1, col2 = st.columns(2)
    # with col2:
        st.subheader("Escenario nacional")
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            for i in range(8):
                valores.append(st.number_input(f"{nombres[i]}", step=0.1, min_value=0.0, max_value=100000.0))
        
        with col1_2:
            for i in range(8, 10):
                valores.append(st.number_input(f"{nombres[i]}", step=0.1, min_value=0.0, max_value=100000.0))

def esenario_internacional():    
    # with col1:
        st.subheader("Escenario internacional")
        col2_1, col2_2 = st.columns(2)
        
        
        with col2_1:
            for i in range(8):
                if i == 2:
                    valores_2.append(st.text_input(f"{nombres_2[i]}"))
                else:
                    valores_2.append(st.number_input(f"{nombres_2[i]}", step=0.01, min_value=0.00, max_value=100000.00))
        
        with col2_2:
            for i in range(8, 16):
                valores_2.append(st.number_input(f"{nombres_2[i]}", step=0.01, min_value=0.00, max_value=100000.00))


if __name__ == "__main__":
    main()

