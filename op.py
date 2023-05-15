import streamlit as st
from pulp import *

def m(valores,valores_2):
    # Aquí va tu método m
    # Crear problema de minimización
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    p_1 = LpVariable("p_1", lowBound=0)
    precio_compra_1=p_1
    cantidad_1=valores[0]
    frecuencia_1=valores[1]
    lt_plantapuerto_1=valores[2]
    dias_cxp_1=valores[3]
    moq_1=valores[4]
    adu_1=valores[5]
    factor_lt_1=valores[6]
    factor_var_1=valores[7]
    estandar_pos_1=valores[8]
    lt_tiempoadmon_1=valores[9]
    lt_puertopuerto_1=valores[10]
    lt_gz_1=valores[11]
    lt_gzplanta_1=valores[12]
    transporte_gz_1=valores[13]

    #campos_1 calculados
    lt_completo_1=lt_tiempoadmon_1+lt_puertopuerto_1+lt_plantapuerto_1+lt_gz_1+lt_gzplanta_1
    lt_logistico_1=lt_puertopuerto_1+lt_plantapuerto_1+lt_gz_1+lt_gzplanta_1
    zona_amarilla_1=lt_plantapuerto_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_plantapuerto_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    taf_gz_1=1.07*precio_compra_1
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_cap_1=(((1+0.12)**(1/52))-1)*lt_plantapuerto_1*costo_inv_1
    costo_maninv_1=(inv_prom_1/estandar_pos_1)*taf_gz_1*(lt_plantapuerto_1/4.3)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1
    costo_unitario_1=costo_total_1/cantidad_1

    
    cantidad=valores_2[0]
    frecuencia=valores_2[1]
    lt_plantapuerto=valores_2[2]
    dias_cxp=valores_2[3]
    moq=valores_2[4]
    adu=valores_2[5]
    factor_lt=valores_2[6]
    factor_var=valores_2[7]
    estandar_pos=valores_2[8]
    lt_tiempoadmon=valores_2[9]
    lt_puertopuerto=valores_2[10]
    lt_gz=valores_2[11]
    lt_gzplanta=valores_2[12]
    transporte_gz=valores_2[13]
    precio_compra=valores_2[14]
    #campos calculados
    lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    lt_logistico=lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    zona_amarilla=lt_plantapuerto*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_plantapuerto*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    taf_gz=1.07*precio_compra
    costo_inv=precio_compra*inv_prom
    costo_cap=(((1+0.12)**(1/52))-1)*lt_plantapuerto*costo_inv
    costo_maninv=(inv_prom/estandar_pos)*taf_gz*(lt_plantapuerto/4.3)
    costo_compra=precio_compra*cantidad
    costo_total=costo_maninv+costo_compra+costo_cap
    costo_unitario_0=costo_total/cantidad


    c_0 = costo_unitario_0  # Costo del producto 0
    c_1 = costo_unitario_1  # Costo del producto 1
    p_0= precio_compra
    # Define las variables de cambio de precio
    #p_0 = LpVariable("p_0", lowBound=0)


    # Agrega restricciones
    #prob += p_0 <= 1
    #prob += p_1 <= 1
    #prob += p_0 >= 0
    prob += p_1 >= 0

    # Define la función objetivo
    #prob += c_1 - c_0 == p_1 - p_0 # Minimiza la diferencia de costos totales
    prob += c_1 - c_0 == 0
    status = prob.solve()
#     return (p_1.value())
    return f"ingreso bueno {p_1.value()}  {valores[0]}"

st.title("Mi aplicación Streamlit")
import streamlit as st

# Definir la disposición en dos columnas
col1, col2 = st.beta_columns(2)
# nombres
nombres=(
"cantidad",
"frecuencia",
"lt_plantapuerto",
"dias_cxp",
"moq",
"adu",
"factor_lt",
"factor_var",
"estandar_pos",
"lt_tiempoadmon",
"lt_puertopuerto",
"lt_gz",
"lt_gzplanta",
"transporte_gz",
"precio_compra")

# Columna izquierda
with col1:
    st.subheader("Escenario nacional")
    # Aquí puedes mostrar los 15 datos correspondientes
    # Crear 15 campos numéricos
    valores = []
    for i in range(14):
        valores.append(st.number_input(f"{nombres[i]}   ", min_value=0, max_value=10000))
    
# Columna derecha
with col2:
    st.subheader("Escenario nacional")
    # Aquí puedes mostrar los 14 datos correspondientes
    # Crear 14 campos numéricos
    valores_2 = []
    for i in range(15):
        valores_2.append(st.number_input(f"{nombres[i]}", min_value=0, max_value=10000))




# Crear botón para ejecutar el métodorun
if st.button("Ejecutar método"):
    resultado = m(valores,valores_2)
    st.write(f"El resultado es: {resultado}")





