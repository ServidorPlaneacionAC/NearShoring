import streamlit as st
from pulp import *

def m(valores):
    # Aquí va tu método m
    # Crear problema de minimización
#     prob = LpProblem("Mi problema de optimización", LpMinimize)
#     p_1 = LpVariable("p_1", lowBound=0)
#     precio_compra_1=p_1
#     cantidad_1=30000
#     frecuencia_1=1
#     lt_plantapuerto_1=1
#     dias_cxp_1=90/7
#     moq_1=1200
#     adu_1=20890
#     factor_lt_1=0.4
#     factor_var_1=0.3
#     estandar_pos_1=350
#     lt_tiempoadmon_1=0
#     lt_puertopuerto_1=0
#     lt_gz_1=0
#     lt_gzplanta_1=0
#     transporte_gz_1=0
#     #campos_1 calculados
#     lt_completo_1=lt_tiempoadmon_1+lt_puertopuerto_1+lt_plantapuerto_1+lt_gz_1+lt_gzplanta_1
#     lt_logistico_1=lt_puertopuerto_1+lt_plantapuerto_1+lt_gz_1+lt_gzplanta_1
#     zona_amarilla_1=lt_plantapuerto_1*adu_1
#     zona_rojabase_1=zona_amarilla_1*factor_lt_1
#     zona_rojaalta_1=zona_rojabase_1*factor_var_1
#     zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_plantapuerto_1*adu_1*factor_lt_1)
#     inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
#     taf_gz_1=1.07*precio_compra_1
#     costo_inv_1=precio_compra_1*inv_prom_1
#     costo_cap_1=(((1+0.12)**(1/52))-1)*lt_plantapuerto_1*costo_inv_1
#     costo_maninv_1=(inv_prom_1/estandar_pos_1)*taf_gz_1*(lt_plantapuerto_1/4.3)
#     costo_compra_1=precio_compra_1*cantidad_1
#     costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1
#     costo_unitario_1=costo_total_1/cantidad_1

#     precio_compra=14000
#     cantidad=30000
#     frecuencia=4
#     lt_plantapuerto=5
#     dias_cxp=90/7
#     moq=24000
#     adu=23800
#     factor_lt=0.1
#     factor_var=0.3
#     estandar_pos=350
#     lt_tiempoadmon=10
#     lt_puertopuerto=8
#     lt_gz=2
#     lt_gzplanta=1
#     transporte_gz=200
#     #campos calculados
#     lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
#     lt_logistico=lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
#     zona_amarilla=lt_plantapuerto*adu
#     zona_rojabase=zona_amarilla*factor_lt
#     zona_rojaalta=zona_rojabase*factor_var
#     zona_verde=max(moq,frecuencia*adu,lt_plantapuerto*adu*factor_lt)
#     inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
#     taf_gz=1.07*precio_compra
#     costo_inv=precio_compra*inv_prom
#     costo_cap=(((1+0.12)**(1/52))-1)*lt_plantapuerto*costo_inv
#     costo_maninv=(inv_prom/estandar_pos)*taf_gz*(lt_plantapuerto/4.3)
#     costo_compra=precio_compra*cantidad
#     costo_total=costo_maninv+costo_compra+costo_cap
#     costo_unitario_0=costo_total/cantidad


#     c_0 = costo_unitario_0  # Costo del producto 0
#     c_1 = costo_unitario_1  # Costo del producto 1
#     p_0= precio_compra
#     # Define las variables de cambio de precio
#     #p_0 = LpVariable("p_0", lowBound=0)


#     # Agrega restricciones
#     #prob += p_0 <= 1
#     #prob += p_1 <= 1
#     #prob += p_0 >= 0
#     prob += p_1 >= 0

#     # Define la función objetivo
#     #prob += c_1 - c_0 == p_1 - p_0 # Minimiza la diferencia de costos totales
#     prob += c_1 - c_0 == 0
#     status = prob.solve()
#     return (p_1.value())
    return "ingreso bueno"

st.title("Mi aplicación Streamlit")

# Crear 15 campos numéricos
valores = []
for i in range(15):
    valores.append(st.number_input(f"Valor {i+1}", min_value=0, max_value=100))

# Crear botón para ejecutar el métodorun
if st.button("Ejecutar método"):
    resultado = m(valores)
    st.write(f"El resultado es: {resultado}")


