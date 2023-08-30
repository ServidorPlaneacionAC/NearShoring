from pulp import *
import streamlit as st


#Falta cambiar el orden en la variabe ebitda

def eva(valores,valores_2,tasa):    # Aquí va tu método m
    # Creamos un objeto de problema de optimización llamado "prob" con objetivo de minimización
    # "Mi problema de optimización" es el nombre del problema, y LpMinimize indica que estamos minimizando
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    # Creamos una variable de optimización llamada "p_1" con límite inferior de 0
    # "p_1" es el nombre de la variable, y lowBound=0 establece el límite inferior en 0
    p_1 = LpVariable("p_1", lowBound=0)
    # Asignamos el valor de la variable de optimización "p_1" a la variable "precio_compra_1"
    precio_compra_1=p_1
    # Los siguientes son parámetros que el usuario ingresa     
    cantidad_1 = valores[0]  # Cantidad de producto
    frecuencia_1 = valores[1]  # Frecuencia de acción
    lt_plantapuerto_1 = valores[2]  # Tiempo planta a puerto
    semanas_cxp_1 = valores[3]  # Semanas de crédito proveedor
    moq_1 = valores[4]  # Cantidad mínima de pedido
    adu_1 = valores[5]  # Días almacenamiento inventario
    factor_lt_1 = valores[6]  # Factor tiempo de tránsito
    factor_var_1 = valores[7]  # Factor de variabilidad
    estandar_pos_1 = valores[8]  # Estándar de posición
    tarifa_alm_1 = valores[9]  # Tarifa de almacenamiento

    
    lt_completo_1 = lt_plantapuerto_1  # Tiempo de tránsito completo igual a tiempo de planta a puerto
    lt_logistico_1 = lt_plantapuerto_1  # Tiempo de tránsito logístico igual a tiempo de planta a puerto
    zona_amarilla_1 = lt_completo_1 * adu_1  # Zona amarilla: Tiempo de tránsito completo multiplicado por adu_1
    zona_rojabase_1 = zona_amarilla_1 * factor_lt_1  # Zona roja base: Zona amarilla multiplicada por factor_lt_1
    zona_rojaalta_1 = zona_rojabase_1 * factor_var_1  # Zona roja alta: Zona roja base multiplicada por factor_var_1
    zona_verde_1 = max(moq_1, frecuencia_1 * adu_1, lt_completo_1 * adu_1 * factor_lt_1)  # Zona verde: Máximo entre moq_1, frecuencia_1 * adu_1 y lt_completo_1 * adu_1 * factor_lt_1
    inv_prom_1 = zona_rojabase_1 + zona_rojaalta_1 + (zona_verde_1 / 2)  # Inventario promedio: Suma de zonas más mitad de zona verde
    inv_prom_sem_1 = inv_prom_1 / adu_1  # Inventario promedio por semana: Inventario promedio dividido por adu_1
    diferencial_1 = lt_logistico_1 - semanas_cxp_1  # Diferencial: Tiempo de tránsito logístico menos semanas de crédito proveedor
    
    taf_gz_1 = 0  # TAF GZ: Valor fijo en 0
    costo_inv_1 = precio_compra_1 * inv_prom_1  # Costo de inventario: Precio de compra por inventario promedio
    costo_nacionalizacion_1 = taf_gz_1 * cantidad_1  # Costo de nacionalización: TAF GZ multiplicado por cantidad_1
    costo_transportegz_planta_1 = (0) * cantidad_1  # Costo de transporte GZ a planta: Valor fijo en 0 multiplicado por cantidad_1
    costo_cap_1 = (diferencial_1 + inv_prom_sem_1) * adu_1 * (((1 + tasa) ** (1/52)) - 1) * precio_compra_1  # Costo de capital: Cálculo con diferenciales, tasa, adu_1 y precio_compra_1
    costo_maninv_1 = (inv_prom_1) * (tarifa_alm_1 / 4.3) * (inv_prom_sem_1)  # Costo de manipulación de inventario: Producto de factores por inventario promedio semanal
    costo_compra_1 = precio_compra_1 * cantidad_1  # Costo de compra: Precio de compra por cantidad
    costo_total_1 = costo_maninv_1 + costo_compra_1 + costo_cap_1 + costo_transportegz_planta_1  # Costo total: Suma de varios costos
    costo_ebitda_1 = costo_maninv_1 + costo_compra_1 + costo_transportegz_planta_1  # Costo EBITDA: Suma de costos relevantes
    costo_unitario_1 = costo_total_1 / cantidad_1  # Costo unitario: Costo total dividido por cantidad
    capital_invertido_1 = ((diferencial_1 + inv_prom_sem_1) * (adu_1)) * (precio_compra_1)  # Capital invertido: Cálculo basado en diferenciales, inventario semanal y precio de compra

    #Escenario actual
    
    cantidad = valores_2[0]  # Cantidad de producto
    frecuencia = valores_2[1]  # Frecuencia de acción
    icoterm = valores_2[2]  # Término de entrega internacional
    lt_plantapuerto = valores_2[3]  # Tiempo de planta a puerto
    semanas_cxp = valores_2[4]  # Semanas de crédito proveedor
    moq = valores_2[5]  # Cantidad mínima de pedido
    adu = valores_2[6]  # Días de almacenamiento en inventario
    factor_lt = valores_2[7]  # Factor de tiempo de tránsito
    factor_var = valores_2[8]  # Factor de variabilidad
    estandar_pos = valores_2[9]  # Estándar de posición
    lt_tiempoadmon = valores_2[10]  # Tiempo de tránsito de aduana
    lt_puertopuerto = valores_2[11]  # Tiempo de puerto a puerto
    lt_gz = valores_2[12]  # Tiempo de tránsito GZ
    lt_gzplanta = valores_2[13]  # Tiempo de tránsito GZ a planta
    tarifa_alm = valores_2[14]  # Tarifa de almacenamiento
    precio_compra = valores_2[15]  # Precio de compra

    # Campos calculados

    # Calcula el tiempo logístico completo sumando los diferentes tiempos involucrados en el proceso.
    lt_completo = lt_tiempoadmon + lt_puertopuerto + lt_plantapuerto + lt_gz + lt_gzplanta
    # Calcula el tiempo logístico basado en el término de entrega internacional (icoterm).
    lt_logistico = icoterm
    if icoterm == "EXWORK":
        lt_logistico = lt_plantapuerto + lt_puertopuerto + lt_gzplanta + lt_gz
    elif icoterm == "FOB":
        lt_logistico = lt_puertopuerto + lt_gzplanta + lt_gz
    else:
        lt_logistico = lt_gzplanta + lt_gz
    # Calcula el valor para la zona amarilla multiplicando el tiempo logístico completo por los días de almacenamiento.
    zona_amarilla = lt_completo * adu
    # Calcula la base para la zona roja multiplicando la zona amarilla por el factor de tiempo de tránsito.
    zona_rojabase = zona_amarilla * factor_lt
    # Calcula la zona roja alta multiplicando la base de la zona roja por el factor de variabilidad.
    zona_rojaalta = zona_rojabase * factor_var
    # Calcula la zona verde tomando el valor máximo entre moq, la frecuencia multiplicada por los días de almacenamiento y el tiempo logístico completo multiplicado por el factor de tiempo de tránsito.
    zona_verde = max(moq, frecuencia * adu, lt_completo * adu * factor_lt)
    # Calcula el inventario promedio sumando la base de la zona roja, la zona roja alta y la mitad de la zona verde.
    inv_prom = zona_rojabase + zona_rojaalta + (zona_verde / 2)
    # Calcula el inventario promedio por semana dividiendo el inventario promedio entre los días de almacenamiento.
    inv_prom_sem = inv_prom / adu
    # Calcula el diferencial entre el tiempo logístico completo y las semanas de crédito proveedor.
    diferencial = lt_completo - semanas_cxp
    # Calcula el valor de taf_gz multiplicando el 7% del precio de compra.
    taf_gz = 0.07 * precio_compra

    
    costo_inv = precio_compra * inv_prom  # Calcula el costo de inventario multiplicando el precio de compra por el inventario promedio.
    costo_nacionalizacion = taf_gz * cantidad  # Calcula el costo de nacionalización multiplicando la tarifa de GZ por la cantidad.
    costo_transportegz_planta = 2 * cantidad  # Calcula el costo de transporte de GZ a planta, considerando dos veces la cantidad.
    costo_cap = (diferencial + inv_prom_sem) * adu * (((1 + tasa) ** (1 / 52)) - 1) * precio_compra  # Calcula el costo de capital tomando en cuenta el diferencial, el inventario promedio por semana, la tasa de interés y el precio de compra.
    costo_maninv = (inv_prom) * (tarifa_alm / 4.3) * (inv_prom_sem)  # Calcula el costo de manipulación de inventario utilizando el inventario promedio, la tarifa de almacenamiento y el inventario promedio por semana.
    costo_compra = precio_compra * cantidad  # Calcula el costo de compra multiplicando el precio de compra por la cantidad.
    costo_total = costo_maninv + costo_compra + costo_cap + costo_nacionalizacion + costo_transportegz_planta  # Calcula el costo total sumando los diferentes costos involucrados.
    costo_ebitda = costo_maninv + costo_compra + costo_nacionalizacion + costo_transportegz_planta  # Calcula el costo EBITDA sumando los costos de manipulación, compra, nacionalización y transporte de GZ a planta.
    costo_unitario_0 = costo_total / cantidad  # Calcula el costo unitario inicial dividiendo el costo total entre la cantidad.
    capital_invertido = ((diferencial + inv_prom_sem) * (adu) * (precio_compra)) + (costo_nacionalizacion)  # Calcula el capital invertido considerando el diferencial, el inventario promedio por semana, los días de almacenamiento y el precio de compra.




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

    return [p_1.value(),value(uodi),value(ebitda),value(eva),value(diferencial_ct),value(capital_invertido_1)]
# nombres
    
def uodi(valores,valores_2,tasa):
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
    zona_amarilla_1=lt_completo_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_logistico_1-semanas_cxp_1
    
    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=0*cantidad_1
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1 +costo_transportegz_planta_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_transportegz_planta_1
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
    zona_amarilla=lt_completo*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_completo-semanas_cxp
    taf_gz=0.07*precio_compra
    
    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=2*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
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
    costo_capital=(diferencial_ct)*(((1+tasa)**(1/52))-1)
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


    # st.write(f"{value(zona_amarilla)}")
    # st.write(f"{value(zona_rojabase)}")
    # st.write(f"{value(zona_rojaalta)}")
    # st.write(f"{value(zona_verde)}")
    
    # st.write(f"{value(zona_amarilla_1)} amarilla nacional")
    # st.write(f"{value(zona_rojabase_1)}")
    # st.write(f"{value(zona_rojaalta_1)}")
    # st.write(f"{value(zona_verde_1)}")
    # st.write(f"{value(lt_completo)} lt_completo")
    # st.write(f"*********************")
    # st.write(f"{value(costo_ebitda)} costo_ebitda internacional  {value(costo_ebitda_1)} costo_ebitda nacional")
    # st.write(f"{value(costo_total)} costo_total internacional  {value(costo_total_1)} costo_total nacional")


    # st.write(f"*********************")
    # st.write(f"{value(costo_transportegz_planta)} costo_transportegz_planta internacional  {value(costo_transportegz_planta_1)} costo_transportegz_planta nacional")
    # st.write(f"{value(costo_inv)} costo_inv internacional  {value(costo_inv_1)} costo_inv nacional")
    # st.write(f"{value(inv_prom)} inv_prom internacional  {value(inv_prom_1)} inv_prom nacional")
    # st.write(f"{value(diferencial)} diferencial internacional  {value(diferencial_1)} diferencial nacional")
    # st.write(f"{value(taf_gz)} taf_gz internacional  {value(taf_gz_1)} taf_gz nacional")
    # st.write(f"{value(costo_maninv)} costo_maninv internacional  {value(costo_maninv_1)} costo_maninv nacional")
    # st.write(f"{value(costo_compra)} costo_compra internacional  {value(costo_compra_1)} costo_compra nacional")
    # st.write(f"{value(costo_cap)} costo_cap internacional  {value(costo_cap_1)} costo_cap nacional")
   

    return [p_1.value(),value(uodi),value(ebitda),value(eva),value(diferencial_ct),value(capital_invertido_1)]


def valores_eva(valores,valores_2,nuevo_precio,tasa):
    
    
    # p_1 = nuevo_precio
    # precio_compra_1=p_1
    # cantidad_1=valores[0]
    # frecuencia_1=valores[1]
    # lt_plantapuerto_1=valores[2]
    # semanas_cxp_1=valores[3]
    # moq_1=valores[4]
    # adu_1=valores[5]
    # factor_lt_1=valores[6]
    # factor_var_1=valores[7]
    # estandar_pos_1=valores[8]
    # tarifa_alm_1=valores[9]


    # #campos_1 calculados

    # lt_completo_1=lt_plantapuerto_1
    # lt_logistico_1=lt_plantapuerto_1
    # zona_amarilla_1=lt_completo_1*adu_1
    # zona_rojabase_1=zona_amarilla_1*factor_lt_1
    # zona_rojaalta_1=zona_rojabase_1*factor_var_1
    # zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    # inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    # inv_prom_sem_1=inv_prom_1/adu_1
    # diferencial_1=lt_logistico_1-semanas_cxp_1

    # taf_gz_1=0
    # costo_inv_1=precio_compra_1*inv_prom_1
    # costo_nacionalizacion_1=taf_gz_1*cantidad_1
    # costo_transportegz_planta_1=0
    # costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    # costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    # costo_compra_1=precio_compra_1*cantidad_1
    # costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1
    # costo_ebitda_1=costo_maninv_1+costo_compra_1
    # costo_unitario_1=costo_total_1/cantidad_1
    # capital_invertido_1=((diferencial_1+inv_prom_sem_1)*(adu_1))*(precio_compra_1)

    # cantidad=valores_2[0]
    # frecuencia=valores_2[1]
    # icoterm = valores_2[2]
    # lt_plantapuerto=valores_2[3]
    # semanas_cxp=valores_2[4]
    # moq=valores_2[5]
    # adu=valores_2[6]
    # factor_lt=valores_2[7]
    # factor_var=valores_2[8]
    # estandar_pos=valores_2[9]
    # lt_tiempoadmon=valores_2[10]
    # lt_puertopuerto=valores_2[11]
    # lt_gz=valores_2[12]
    # lt_gzplanta=valores_2[13]
    # tarifa_alm=valores_2[14]
    # precio_compra=valores_2[15]
    # #campos calculados

    # lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    # lt_logistico= icoterm  
    # if icoterm == "EXWORK":
    #     lt_logistico = lt_plantapuerto+lt_puertopuerto+lt_gzplanta+lt_gz
    # elif icoterm == "FOB":
    #     lt_logistico = lt_puertopuerto+lt_gzplanta+lt_gz
    # else:
    #     lt_logistico = lt_gzplanta+lt_gz
    # zona_amarilla=lt_completo_1*adu
    # zona_rojabase=zona_amarilla*factor_lt
    # zona_rojaalta=zona_rojabase*factor_var
    # zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    # inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    # inv_prom_sem=inv_prom/adu
    # diferencial=lt_logistico-semanas_cxp
    # taf_gz=0.07*precio_compra

    # costo_inv=precio_compra*inv_prom
    # costo_nacionalizacion=taf_gz*cantidad
    # costo_transportegz_planta=200*cantidad
    # costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
    # costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    # costo_compra=precio_compra*cantidad
    # costo_total=costo_maninv+costo_compra+costo_cap+costo_nacionalizacion+costo_transportegz_planta
    # costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    # costo_unitario_0=costo_total/cantidad
    # capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)

 # Aquí va tu método m
    # Crear problema de minimización
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    p_1 = nuevo_precio
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
    zona_amarilla_1=lt_completo_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_logistico_1-semanas_cxp_1
    
    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=200*cantidad_1
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1 +costo_transportegz_planta_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_transportegz_planta_1
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
    zona_amarilla=lt_completo*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_completo-semanas_cxp
    taf_gz=0.07*precio_compra
    
    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=200*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
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
    costo_capital=(diferencial_ct)*(((1+tasa)**(1/52))-1)
    eva=uodi-costo_capital
    #roic=uodi/diferencial_ct

    c_0 = costo_unitario_0  # Costo del producto 0
    c_1 = costo_unitario_1  # Costo del producto 1
    p_0= precio_compra
#     return (p_1.value())
    return [p_1,(uodi),(ebitda),(eva),(diferencial_ct),(capital_invertido_1)]
# nombres

def valores_uodi(valores,valores_2,nuevo_precio,tasa):
    # p_1 = nuevo_precio
    # precio_compra_1=p_1
    # cantidad_1=valores[0]
    # frecuencia_1=valores[1]
    # lt_plantapuerto_1=valores[2]
    # semanas_cxp_1=valores[3]
    # moq_1=valores[4]
    # adu_1=valores[5]
    # factor_lt_1=valores[6]
    # factor_var_1=valores[7]
    # estandar_pos_1=valores[8]
    # tarifa_alm_1=valores[9]
    
    # #campos_1 calculados
    
    # lt_completo_1=lt_plantapuerto_1
    # lt_logistico_1=lt_plantapuerto_1
    # zona_amarilla_1=lt_completo_1*adu_1
    # zona_rojabase_1=zona_amarilla_1*factor_lt_1
    # zona_rojaalta_1=zona_rojabase_1*factor_var_1
    # zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    # inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    # inv_prom_sem_1=inv_prom_1/adu_1
    # diferencial_1=lt_logistico_1-semanas_cxp_1
    
    # taf_gz_1=0
    # costo_inv_1=precio_compra_1*inv_prom_1
    # costo_nacionalizacion_1=taf_gz_1*cantidad_1
    # costo_transportegz_planta_1=0
    # costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    # costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    # costo_compra_1=precio_compra_1*cantidad_1
    # costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1
    # costo_ebitda_1=costo_maninv_1+costo_compra_1
    # costo_unitario_1=costo_total_1/cantidad_1
    # capital_invertido_1=((diferencial_1+inv_prom_sem_1)*(adu_1))*(precio_compra_1)
    
    # cantidad=valores_2[0]
    # frecuencia=valores_2[1]
    # icoterm = valores_2[2]
    # lt_plantapuerto=valores_2[3]
    # semanas_cxp=valores_2[4]
    # moq=valores_2[5]
    # adu=valores_2[6]
    # factor_lt=valores_2[7]
    # factor_var=valores_2[8]
    # estandar_pos=valores_2[9]
    # lt_tiempoadmon=valores_2[10]
    # lt_puertopuerto=valores_2[11]
    # lt_gz=valores_2[12]
    # lt_gzplanta=valores_2[13]
    # tarifa_alm=valores_2[14]
    # precio_compra=valores_2[15]
    # #campos calculados
    
    # lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    # lt_logistico= icoterm  
    # if icoterm == "EXWORK":
    #     lt_logistico = lt_plantapuerto+lt_puertopuerto+lt_gzplanta+lt_gz
    # elif icoterm == "FOB":
    #     lt_logistico = lt_puertopuerto+lt_gzplanta+lt_gz
    # else:
    #     lt_logistico = lt_gzplanta+lt_gz
    # zona_amarilla=lt_completo_1*adu
    # zona_rojabase=zona_amarilla*factor_lt
    # zona_rojaalta=zona_rojabase*factor_var
    # zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    # inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    # inv_prom_sem=inv_prom/adu
    # diferencial=lt_logistico-semanas_cxp
    # taf_gz=0.07*precio_compra
    
    # costo_inv=precio_compra*inv_prom
    # costo_nacionalizacion=taf_gz*cantidad
    # costo_transportegz_planta=200*cantidad
    # costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
    # costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    # costo_compra=precio_compra*cantidad
    # costo_total=costo_maninv+costo_compra+costo_cap+costo_nacionalizacion+costo_transportegz_planta
    # costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    # costo_unitario_0=costo_total/cantidad
    # capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)

 # Aquí va tu método m
    # Crear problema de minimización
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    p_1 = nuevo_precio
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
    zona_amarilla_1=lt_completo_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_completo_1-semanas_cxp_1
    
    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=0*cantidad_1
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1 +costo_transportegz_planta_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_transportegz_planta_1
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
    zona_amarilla=lt_completo*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_completo-semanas_cxp
    taf_gz=0.07*precio_compra
    
    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=2*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
    costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    costo_compra=precio_compra*cantidad
    costo_total=costo_maninv+costo_compra+costo_cap+costo_nacionalizacion+costo_transportegz_planta
    costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    costo_unitario_0=costo_total/cantidad
    capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)


    #calculo variables financieras

    ebitda=-costo_ebitda_1+costo_ebitda
    impuestos=ebitda*0.26
    uodi=ebitda-impuestos
    diferencial_ct=capital_invertido-capital_invertido_1
    costo_capital=(diferencial_ct)*(((1+tasa)**(1/52))-1)
    eva=uodi-costo_capital
    #roic=uodi/diferencial_ct
    c_0 = costo_unitario_0  # Costo del producto 0
    c_1 = costo_unitario_1  # Costo del producto 1
    p_0= precio_compra

    # st.write(f"{diferencial_ct}  diferencial_ct")
    # st.write(f"{uodi}  uodi")
    # st.write(f"{ebitda}  ebitda")
    # st.write(f"{costo_ebitda_1}  costo_ebitda_1")
    # st.write(f"{costo_capital}  costo_capital")
#     return (p_1.value())
    return [p_1,(uodi),(ebitda),(eva),(diferencial_ct),(capital_invertido_1)]

def eva_int(valores,valores_2,tasa):
    
    # prob = LpProblem("Mi problema de optimización", LpMinimize)
    # p_1 = LpVariable("p_1", lowBound=0)
    # precio_compra_1=p_1
    # cantidad_1=valores[0]
    # frecuencia_1=valores[1]
    # icoterm_1 = valores[2]
    # lt_plantapuerto_1=valores[3]
    # semanas_cxp_1=valores[4]
    # moq_1=valores[5]
    # adu_1=valores[6]
    # factor_lt_1=valores[7]
    # factor_var_1=valores[8]
    # estandar_pos_1=valores[9]
    # lt_tiempoadmon_1=valores[10]
    # lt_puertopuerto_1=valores[11]
    # lt_gz_1=valores[12]
    # lt_gzplanta_1=valores[13]
    # tarifa_alm_1=valores[14]
    
    # #campos calculados

    # lt_completo_1=lt_tiempoadmon_1+lt_puertopuerto_1+lt_plantapuerto_1+lt_gz_1+lt_gzplanta_1
    # lt_logistico_1= icoterm_1  
    # if icoterm_1 == "EXWORK":
    #     lt_logistico_1 = lt_plantapuerto_1+lt_puertopuerto_1+lt_gzplanta_1+lt_gz_1
    # elif icoterm_1 == "FOB":
    #     lt_logistico_1 = lt_puertopuerto_1+lt_gzplanta_1+lt_gz_1
    # else:
    #     lt_logistico_1 = lt_gzplanta_1+lt_gz_1
    # zona_amarilla_1=lt_completo_1*adu_1
    # zona_rojabase_1=zona_amarilla_1*factor_lt_1
    # zona_rojaalta_1=zona_rojabase_1*factor_var_1
    # zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo*adu_1*factor_lt_1)
    # inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    # inv_prom_sem_1=inv_prom_1/adu_1
    # diferencial_1=lt_logistico_1-semanas_cxp_1
    # taf_gz_1=0.07*precio_compra_1

    # costo_inv_1=precio_compra_1*inv_prom_1
    # costo_nacionalizacion_1=taf_gz_1*cantidad_1
    # costo_transportegz_planta_1=200*cantidad_1
    # costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    # costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    # costo_compra_1=precio_compra_1*cantidad_1
    # costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1+costo_nacionalizacion_1+costo_transportegz_planta_1
    # costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_nacionalizacion_1+costo_transportegz_planta_1
    # costo_unitario_1=costo_total_1/cantidad_1
    # capital_invertido_1=((diferencial_1+inv_prom_sem_1)*(adu_1)*(precio_compra_1))+(costo_nacionalizacion_1)

    # cantidad=valores_2[0]
    # frecuencia=valores_2[1]
    # icoterm = valores_2[2]
    # lt_plantapuerto=valores_2[3]
    # semanas_cxp=valores_2[4]
    # moq=valores_2[5]
    # adu=valores_2[6]
    # factor_lt=valores_2[7]
    # factor_var=valores_2[8]
    # estandar_pos=valores_2[9]
    # lt_tiempoadmon=valores_2[10]
    # lt_puertopuerto=valores_2[11]
    # lt_gz=valores_2[12]
    # lt_gzplanta=valores_2[13]
    # tarifa_alm=valores_2[14]
    # precio_compra=valores_2[15]
    # #campos calculados

    # lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    # lt_logistico= icoterm  
    # if icoterm == "EXWORK":
    #     lt_logistico = lt_plantapuerto+lt_puertopuerto+lt_gzplanta+lt_gz
    # else:
    #     if icoterm == "FOB":
    #         lt_logistico = lt_puertopuerto+lt_gzplanta+lt_gz
    #     else:
    #         lt_logistico = lt_gzplanta+lt_gz
    # zona_amarilla=lt_completo*adu
    # zona_rojabase=zona_amarilla*factor_lt
    # zona_rojaalta=zona_rojabase*factor_var
    # zona_verde=max(moq,frecuencia*adu,lt_completo*adu*factor_lt)
    # inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    # inv_prom_sem=inv_prom/adu
    # diferencial=lt_logistico-semanas_cxp
    # taf_gz=0.07*precio_compra

    # costo_inv=precio_compra*inv_prom
    # costo_nacionalizacion=taf_gz*cantidad
    # costo_transportegz_planta=200*cantidad
    # costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
    # costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    # costo_compra=precio_compra*cantidad
    # costo_total=costo_maninv+costo_compra+costo_cap+costo_nacionalizacion+costo_transportegz_planta
    # costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    # costo_unitario_0=costo_total/cantidad
    # capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)

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
    zona_amarilla_1=lt_completo_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_logistico_1-semanas_cxp_1
    
    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=200*cantidad_1
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1 +costo_transportegz_planta_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_transportegz_planta_1
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
    zona_amarilla=lt_completo*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_completo-semanas_cxp
    taf_gz=0.07*precio_compra
    
    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=200*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
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
    costo_capital=(diferencial_ct)*(((1+tasa)**(1/52))-1)
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
    return [p_1.value(),value(uodi),value(ebitda),value(eva),value(diferencial_ct),value(capital_invertido_1)]
# nombres
def uodi_int(valores,valores_2,tasa):    
    # prob = LpProblem("Mi problema de optimización", LpMinimize)
    # p_1 = LpVariable("p_1", lowBound=0)
    # precio_compra_1=p_1
    # cantidad_1=valores[0]
    # frecuencia_1=valores[1]
    # icoterm_1 = valores[2]
    # lt_plantapuerto_1=valores[3]
    # semanas_cxp_1=valores[4]
    # moq_1=valores[5]
    # adu_1=valores[6]
    # factor_lt_1=valores[7]
    # factor_var_1=valores[8]
    # estandar_pos_1=valores[9]
    # lt_tiempoadmon_1=valores[10]
    # lt_puertopuerto_1=valores[11]
    # lt_gz_1=valores[12]
    # lt_gzplanta_1=valores[13]
    # tarifa_alm_1=valores[14]
    
    # #campos calculados

    # lt_completo_1=lt_tiempoadmon_1+lt_puertopuerto_1+lt_plantapuerto_1+lt_gz_1+lt_gzplanta_1
    # lt_logistico_1= icoterm_1  
    # if icoterm_1 == "EXWORK":
    #     lt_logistico_1 = lt_plantapuerto_1+lt_puertopuerto_1+lt_gzplanta_1+lt_gz_1
    # elif icoterm_1 == "FOB":
    #     lt_logistico_1 = lt_puertopuerto_1+lt_gzplanta_1+lt_gz_1
    # else:
    #     lt_logistico_1 = lt_gzplanta_1+lt_gz_1
    # zona_amarilla_1=lt_completo*adu_1
    # zona_rojabase_1=zona_amarilla_1*factor_lt_1
    # zona_rojaalta_1=zona_rojabase_1*factor_var_1
    # zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo*adu_1*factor_lt_1)
    # inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    # inv_prom_sem_1=inv_prom_1/adu_1
    # diferencial_1=lt_logistico_1-semanas_cxp_1
    # taf_gz_1=0.07*precio_compra_1

    # costo_inv_1=precio_compra_1*inv_prom_1
    # costo_nacionalizacion_1=taf_gz_1*cantidad_1
    # costo_transportegz_planta_1=200*cantidad_1
    # costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    # costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    # costo_compra_1=precio_compra_1*cantidad_1
    # costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1+costo_nacionalizacion_1+costo_transportegz_planta_1
    # costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_nacionalizacion_1+costo_transportegz_planta_1
    # costo_unitario_1=costo_total_1/cantidad_1
    # capital_invertido_1=((diferencial_1+inv_prom_sem_1)*(adu_1)*(precio_compra_1))+(costo_nacionalizacion_1)

    # cantidad=valores_2[0]
    # frecuencia=valores_2[1]
    # icoterm = valores_2[2]
    # lt_plantapuerto=valores_2[3]
    # semanas_cxp=valores_2[4]
    # moq=valores_2[5]
    # adu=valores_2[6]
    # factor_lt=valores_2[7]
    # factor_var=valores_2[8]
    # estandar_pos=valores_2[9]
    # lt_tiempoadmon=valores_2[10]
    # lt_puertopuerto=valores_2[11]
    # lt_gz=valores_2[12]
    # lt_gzplanta=valores_2[13]
    # tarifa_alm=valores_2[14]
    # precio_compra=valores_2[15]
    # #campos calculados

    # lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    # lt_logistico= icoterm  
    # if icoterm == "EXWORK":
    #     lt_logistico = lt_plantapuerto+lt_puertopuerto+lt_gzplanta+lt_gz
    # elif icoterm == "FOB":
    #     lt_logistico = lt_puertopuerto+lt_gzplanta+lt_gz
    # else:
    #     lt_logistico = lt_gzplanta+lt_gz
    # zona_amarilla=lt_completo*adu
    # zona_rojabase=zona_amarilla*factor_lt
    # zona_rojaalta=zona_rojabase*factor_var
    # zona_verde=max(moq,frecuencia*adu,lt_completo*adu*factor_lt)
    # inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    # inv_prom_sem=inv_prom/adu
    # diferencial=lt_logistico-semanas_cxp
    # taf_gz=0.07*precio_compra

    # costo_inv=precio_compra*inv_prom
    # costo_nacionalizacion=taf_gz*cantidad
    # costo_transportegz_planta=200*cantidad
    # costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
    # costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    # costo_compra=precio_compra*cantidad
    # costo_total=costo_maninv+costo_compra+costo_nacionalizacion+costo_cap+costo_transportegz_planta
    # costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    # costo_unitario_0=costo_total/cantidad
    # capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)

 # Aquí va tu método m
    # Crear problema de minimización
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    # p_1 = LpVariable("p_1", lowBound=0)
    # precio_compra_1=p_1
    # cantidad_1=valores[0]
    # frecuencia_1=valores[1]
    # lt_plantapuerto_1=valores[2]
    # semanas_cxp_1=valores[3]
    # moq_1=valores[4]
    # adu_1=valores[5]
    # factor_lt_1=valores[6]
    # factor_var_1=valores[7]
    # estandar_pos_1=valores[8]
    # tarifa_alm_1=valores[9]
    

    p_1 = LpVariable("p_1", lowBound=0)
    precio_compra_1=p_1
    cantidad_1=valores[0]
    frecuencia_1=valores[1]
    icoterm_1 = valores[2]
    lt_plantapuerto_1=valores[3]
    semanas_cxp_1=valores[4]
    moq_1=valores[5]
    adu_1=valores[6]
    factor_lt_1=valores[7]
    factor_var_1=valores[8]
    estandar_pos_1=valores[9]
    lt_tiempoadmon_1=valores[10]
    lt_puertopuerto_1=valores[11]
    lt_gz_1=valores[12]
    lt_gzplanta_1=valores[13]
    tarifa_alm_1=valores[14]

    #campos_1 calculados
    
    lt_completo_1=lt_puertopuerto_1 # lt_plantapuerto_1
    lt_logistico_1=lt_puertopuerto_1 #lt_plantapuerto_1
    zona_amarilla_1=lt_completo_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_logistico_1-semanas_cxp_1
    
    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=200*cantidad_1
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1 +costo_transportegz_planta_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_transportegz_planta_1
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
    zona_amarilla=lt_completo*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_completo-semanas_cxp
    taf_gz=0.07*precio_compra
    
    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=200*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
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
    costo_capital=(diferencial_ct)*(((1+tasa)**(1/52))-1)
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
    return [p_1.value(),value(uodi),value(ebitda),value(eva),value(diferencial_ct),value(capital_invertido_1)]




#----------------------------------------------------



def valores_eva_int(valores,valores_2,nuevo_precio,tasa):
    
    # p_1 = nuevo_precio
    # precio_compra_1=p_1
    # cantidad_1=valores[0]
    # frecuencia_1=valores[1]
    # icoterm_1 = valores[2]
    # lt_plantapuerto_1=valores[3]
    # semanas_cxp_1=valores[4]
    # moq_1=valores[5]
    # adu_1=valores[6]
    # factor_lt_1=valores[7]
    # factor_var_1=valores[8]
    # estandar_pos_1=valores[9]
    # lt_tiempoadmon_1=valores[10]
    # lt_puertopuerto_1=valores[11]
    # lt_gz_1=valores[12]
    # lt_gzplanta_1=valores[13]
    # tarifa_alm_1=valores[14]
    
    # #campos calculados

    # lt_completo_1=lt_tiempoadmon_1+lt_puertopuerto_1+lt_plantapuerto_1+lt_gz_1+lt_gzplanta_1
    # lt_logistico_1= icoterm_1  
    # if icoterm_1 == "EXWORK":
    #     lt_logistico_1 = lt_plantapuerto_1+lt_puertopuerto_1+lt_gzplanta_1+lt_gz_1
    # elif icoterm_1 == "FOB":
    #     lt_logistico_1 = lt_puertopuerto_1+lt_gzplanta_1+lt_gz_1
    # else:
    #     lt_logistico_1 = lt_gzplanta_1+lt_gz_1
    # zona_amarilla_1=lt_completo*adu_1
    # zona_rojabase_1=zona_amarilla_1*factor_lt_1
    # zona_rojaalta_1=zona_rojabase_1*factor_var_1
    # zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo*adu_1*factor_lt_1)
    # inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    # inv_prom_sem_1=inv_prom_1/adu_1
    # diferencial_1=lt_logistico_1-semanas_cxp_1
    # taf_gz_1=0.07*precio_compra_1

    # costo_inv_1=precio_compra_1*inv_prom_1
    # costo_nacionalizacion_1=taf_gz_1*cantidad_1
    # costo_transportegz_planta_1=200*cantidad_1
    # costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    # costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    # costo_compra_1=precio_compra_1*cantidad_1
    # costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1+costo_nacionalizacion_1+costo_transportegz_planta_1
    # costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_nacionalizacion_1+costo_transportegz_planta_1
    # costo_unitario_1=costo_total_1/cantidad_1
    # capital_invertido_1=((diferencial_1+inv_prom_sem_1)*(adu_1)*(precio_compra_1))+(costo_nacionalizacion_1)

    # cantidad=valores_2[0]
    # frecuencia=valores_2[1]
    # icoterm = valores_2[2]
    # lt_plantapuerto=valores_2[3]
    # semanas_cxp=valores_2[4]
    # moq=valores_2[5]
    # adu=valores_2[6]
    # factor_lt=valores_2[7]
    # factor_var=valores_2[8]
    # estandar_pos=valores_2[9]
    # lt_tiempoadmon=valores_2[10]
    # lt_puertopuerto=valores_2[11]
    # lt_gz=valores_2[12]
    # lt_gzplanta=valores_2[13]
    # tarifa_alm=valores_2[14]
    # precio_compra=valores_2[15]
    # #campos calculados

    # lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    # lt_logistico= icoterm  
    # if icoterm == "EXWORK":
    #     lt_logistico = lt_plantapuerto+lt_puertopuerto+lt_gzplanta+lt_gz
    # elif icoterm == "FOB":
    #     lt_logistico = lt_puertopuerto+lt_gzplanta+lt_gz
    # else:
    #     lt_logistico = lt_gzplanta+lt_gz
    # zona_amarilla=lt_completo*adu
    # zona_rojabase=zona_amarilla*factor_lt
    # zona_rojaalta=zona_rojabase*factor_var
    # zona_verde=max(moq,frecuencia*adu,lt_completo*adu*factor_lt)
    # inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    # inv_prom_sem=inv_prom/adu
    # diferencial=lt_logistico-semanas_cxp
    # taf_gz=0.07*precio_compra

    # costo_inv=precio_compra*inv_prom
    # costo_nacionalizacion=taf_gz*cantidad
    # costo_transportegz_planta=200*cantidad
    # costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
    # costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    # costo_compra=precio_compra*cantidad
    # costo_total=costo_maninv+costo_compra+costo_cap+costo_nacionalizacion+costo_transportegz_planta
    # costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    # costo_unitario_0=costo_total/cantidad
    # capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)

 # Aquí va tu método m
    # Crear problema de minimización
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    p_1 = nuevo_precio
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
    zona_amarilla_1=lt_completo_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_logistico_1-semanas_cxp_1
    
    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=200*cantidad_1
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1 +costo_transportegz_planta_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_transportegz_planta_1
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
    zona_amarilla=lt_completo*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_completo-semanas_cxp
    taf_gz=0.07*precio_compra
    
    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=200*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
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
    costo_capital=(diferencial_ct)*(((1+tasa)**(1/52))-1)
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
    # prob += eva >= 0

    # Define la función objetivo
    #prob += c_1 - c_0 == p_1 - p_0 # Minimiza la diferencia de costos totales
    # prob += eva == 0
    # status = prob.solve()
#     return (p_1.value())
    return [p_1,(uodi),(ebitda),(eva),(diferencial_ct),(capital_invertido_1)]
# nombres

def valores_uodi_int(valores,valores_2,nuevo_precio,tasa):    
    # p_1 = nuevo_precio
    # precio_compra_1=p_1
    # cantidad_1=valores[0]
    # frecuencia_1=valores[1]
    # icoterm_1 = valores[2]
    # lt_plantapuerto_1=valores[3]
    # semanas_cxp_1=valores[4]
    # moq_1=valores[5]
    # adu_1=valores[6]
    # factor_lt_1=valores[7]
    # factor_var_1=valores[8]
    # estandar_pos_1=valores[9]
    # lt_tiempoadmon_1=valores[10]
    # lt_puertopuerto_1=valores[11]
    # lt_gz_1=valores[12]
    # lt_gzplanta_1=valores[13]
    # tarifa_alm_1=valores[14]
    
    # #campos calculados

    # lt_completo_1=lt_tiempoadmon_1+lt_puertopuerto_1+lt_plantapuerto_1+lt_gz_1+lt_gzplanta_1
    # lt_logistico_1= icoterm_1  
    # if icoterm_1 == "EXWORK":
    #     lt_logistico_1 = lt_plantapuerto_1+lt_puertopuerto_1+lt_gzplanta_1+lt_gz_1
    # elif icoterm_1 == "FOB":
    #     lt_logistico_1 = lt_puertopuerto_1+lt_gzplanta_1+lt_gz_1
    # else:
    #     lt_logistico_1 = lt_gzplanta_1+lt_gz_1
    # zona_amarilla_1=lt_completo*adu_1
    # zona_rojabase_1=zona_amarilla_1*factor_lt_1
    # zona_rojaalta_1=zona_rojabase_1*factor_var_1
    # zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo*adu_1*factor_lt_1)
    # inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    # inv_prom_sem_1=inv_prom_1/adu_1
    # diferencial_1=lt_logistico_1-semanas_cxp_1
    # taf_gz_1=0.07*precio_compra_1

    # costo_inv_1=precio_compra_1*inv_prom_1
    # costo_nacionalizacion_1=taf_gz_1*cantidad_1
    # costo_transportegz_planta_1=200*cantidad_1
    # costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    # costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    # costo_compra_1=precio_compra_1*cantidad_1
    # costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1+costo_nacionalizacion_1+costo_transportegz_planta_1
    # costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_nacionalizacion_1+costo_transportegz_planta_1
    # costo_unitario_1=costo_total_1/cantidad_1
    # capital_invertido_1=((diferencial_1+inv_prom_sem_1)*(adu_1)*(precio_compra_1))+(costo_nacionalizacion_1)

    # cantidad=valores_2[0]
    # frecuencia=valores_2[1]
    # icoterm = valores_2[2]
    # lt_plantapuerto=valores_2[3]
    # semanas_cxp=valores_2[4]
    # moq=valores_2[5]
    # adu=valores_2[6]
    # factor_lt=valores_2[7]
    # factor_var=valores_2[8]
    # estandar_pos=valores_2[9]
    # lt_tiempoadmon=valores_2[10]
    # lt_puertopuerto=valores_2[11]
    # lt_gz=valores_2[12]
    # lt_gzplanta=valores_2[13]
    # tarifa_alm=valores_2[14]
    # precio_compra=valores_2[15]
    # #campos calculados

    # lt_completo=lt_tiempoadmon+lt_puertopuerto+lt_plantapuerto+lt_gz+lt_gzplanta
    # lt_logistico= icoterm  
    # if icoterm == "EXWORK":
    #     lt_logistico = lt_plantapuerto+lt_puertopuerto+lt_gzplanta+lt_gz
    # elif icoterm == "FOB":
    #     lt_logistico = lt_puertopuerto+lt_gzplanta+lt_gz
    # else:
    #     lt_logistico = lt_gzplanta+lt_gz
    # zona_amarilla=lt_completo*adu
    # zona_rojabase=zona_amarilla*factor_lt
    # zona_rojaalta=zona_rojabase*factor_var
    # zona_verde=max(moq,frecuencia*adu,lt_completo*adu*factor_lt)
    # inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    # inv_prom_sem=inv_prom/adu
    # diferencial=lt_logistico-semanas_cxp
    # taf_gz=0.07*precio_compra

    # costo_inv=precio_compra*inv_prom
    # costo_nacionalizacion=taf_gz*cantidad
    # costo_transportegz_planta=200*cantidad
    # costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
    # costo_maninv=(inv_prom)*(tarifa_alm/4.3)*(inv_prom_sem)
    # costo_compra=precio_compra*cantidad
    # costo_total=costo_maninv+costo_compra+costo_nacionalizacion+costo_cap+costo_transportegz_planta
    # costo_ebitda=costo_maninv+costo_compra+costo_nacionalizacion+costo_transportegz_planta
    # costo_unitario_0=costo_total/cantidad
    # capital_invertido=((diferencial+inv_prom_sem)*(adu)*(precio_compra))+(costo_nacionalizacion)


 # Aquí va tu método m
    # Crear problema de minimización
    prob = LpProblem("Mi problema de optimización", LpMinimize)
    # p_1 = nuevo_precio
    # precio_compra_1=p_1
    # cantidad_1=valores[0]
    # frecuencia_1=valores[1]
    # lt_plantapuerto_1=valores[2]
    # semanas_cxp_1=valores[3]
    # moq_1=valores[4]
    # adu_1=valores[5]
    # factor_lt_1=valores[6]
    # factor_var_1=valores[7]
    # estandar_pos_1=valores[8]
    # tarifa_alm_1=valores[9]
    

    p_1 = nuevo_precio
    precio_compra_1=p_1
    cantidad_1=valores[0]
    frecuencia_1=valores[1]
    icoterm_1 = valores[2]
    lt_plantapuerto_1=valores[3]
    semanas_cxp_1=valores[4]
    moq_1=valores[5]
    adu_1=valores[6]
    factor_lt_1=valores[7]
    factor_var_1=valores[8]
    estandar_pos_1=valores[9]
    lt_tiempoadmon_1=valores[10]
    lt_puertopuerto_1=valores[11]
    lt_gz_1=valores[12]
    lt_gzplanta_1=valores[13]
    tarifa_alm_1=valores[14]
    

    #campos_1 calculados
    
    lt_completo_1=lt_plantapuerto_1
    lt_logistico_1=lt_plantapuerto_1
    zona_amarilla_1=lt_completo_1*adu_1
    zona_rojabase_1=zona_amarilla_1*factor_lt_1
    zona_rojaalta_1=zona_rojabase_1*factor_var_1
    zona_verde_1=max(moq_1,frecuencia_1*adu_1,lt_completo_1*adu_1*factor_lt_1)
    inv_prom_1=zona_rojabase_1+zona_rojaalta_1+(zona_verde_1/2)
    inv_prom_sem_1=inv_prom_1/adu_1
    diferencial_1=lt_logistico_1-semanas_cxp_1
    
    taf_gz_1=0
    costo_inv_1=precio_compra_1*inv_prom_1
    costo_nacionalizacion_1=taf_gz_1*cantidad_1
    costo_transportegz_planta_1=200*cantidad_1
    costo_cap_1=(diferencial_1+inv_prom_sem_1)*adu_1*(((1+tasa)**(1/52))-1)*precio_compra_1
    costo_maninv_1=(inv_prom_1)*(tarifa_alm_1/4.3)*(inv_prom_sem_1)
    costo_compra_1=precio_compra_1*cantidad_1
    costo_total_1=costo_maninv_1+costo_compra_1+costo_cap_1 +costo_transportegz_planta_1
    costo_ebitda_1=costo_maninv_1+costo_compra_1+costo_transportegz_planta_1
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
    zona_amarilla=lt_completo*adu
    zona_rojabase=zona_amarilla*factor_lt
    zona_rojaalta=zona_rojabase*factor_var
    zona_verde=max(moq,frecuencia*adu,lt_completo_1*adu*factor_lt)
    inv_prom=zona_rojabase+zona_rojaalta+(zona_verde/2)
    inv_prom_sem=inv_prom/adu
    diferencial=lt_completo-semanas_cxp
    taf_gz=0.07*precio_compra
    
    costo_inv=precio_compra*inv_prom
    costo_nacionalizacion=taf_gz*cantidad
    costo_transportegz_planta=200*cantidad
    costo_cap=(diferencial+inv_prom_sem)*adu*(((1+tasa)**(1/52))-1)*precio_compra
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
    costo_capital=(diferencial_ct)*(((1+tasa)**(1/52))-1)
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
    # prob += uodi >= 0

    # Define la función objetivo
    #prob += c_1 - c_0 == p_1 - p_0 # Minimiza la diferencia de costos totales
    # prob += uodi == 0
    # status = prob.solve()
#     return (p_1.value())
    return [p_1,(uodi),(ebitda),(eva),(diferencial_ct),(capital_invertido_1)]


