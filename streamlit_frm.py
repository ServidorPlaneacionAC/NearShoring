import streamlit as st
from streamlit import session_state
import matplotlib.pyplot as plt
import mplcursors
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import utils as calculos

class streamlit_frm:
  def __init__(self,valor_en_pesos,trm=4800.00,tasa=0.12):
        self.error=True
        self.trm=trm
        self.valor_en_pesos=valor_en_pesos 
        self.tasa=tasa
    
  def resultados(self,resultado,valores,valores_2,costo_capital):
    
    st.subheader("Resultado óptimo")    
    tabla_resultado=pd.DataFrame(
                                 [[resultado[0][0],
                                   "{:.2f}%".format((resultado[0][0]-self.valor_en_pesos)/self.valor_en_pesos*100),
                                    -round(resultado[0][1],2),
                                    -round(resultado[0][2],2),
                                    -round(resultado[0][3],2),
                                    -round(0 if resultado[0][4] == 0 else resultado[0][1]/resultado[0][4],2),
                                    round(resultado[0][5],2)]],
                                    
                                 columns=['Precio a pagar','variación respecto al original','UODI','EBITDA','EVA','ROIC','CP'])
    st.write(tabla_resultado)
    
    checkbox_ingresar_valor_negocicion = st.checkbox("Indicar un precio de negociación para evaluar los indicadores de flujo")
    if checkbox_ingresar_valor_negocicion:
        nuevo_precio=st.number_input("Precio negociación", step=0.1, min_value=0.0, max_value=100000.0, value=1.0)
        if costo_capital:
            resultados_nuevo_precio=calculos.valores_eva(valores,valores_2,nuevo_precio,self.tasa)
        else:
            resultados_nuevo_precio=calculos.valores_uodi(valores,valores_2,nuevo_precio)
        nueva_tabla_resultado=pd.DataFrame(
                                    [[resultados_nuevo_precio[0],
                                    "{:.2f}%".format((resultados_nuevo_precio[0]-self.valor_en_pesos)/self.valor_en_pesos*100),
                                        -round(resultados_nuevo_precio[1],2),
                                        -round(resultados_nuevo_precio[2],2),
                                        -round(resultados_nuevo_precio[3],2),
                                        -round(0 if resultados_nuevo_precio[4] == 0 else resultados_nuevo_precio[1]/resultados_nuevo_precio[4],2),
                                        round(resultados_nuevo_precio[5],2)]], 
                                    columns=['Precio a pagar','variación respecto al original','UODI','EBITDA','EVA','ROIC','CP'])
        st.write(nueva_tabla_resultado)


    st.subheader("Resultados Cercanos")    
    tabla_resultado=pd.DataFrame(
                                 [[resultado[i][0],
                                   "{:.2f}%".format((resultado[i][0]-self.valor_en_pesos)/self.valor_en_pesos*100),
                                    -round(resultado[i][1],2),
                                    -round(resultado[i][2],2),
                                    -round(resultado[i][3],2),
                                    -round(0 if resultado[i][4] == 0 else resultado[i][1]/resultado[i][4],2),
                                    round(resultado[i][5],2)] for i in range(len(resultado))] 
                                 columns=['Precio a pagar','variación respecto al original','UODI','EBITDA','EVA','ROIC','CP'])
    st.write(tabla_resultado[1:]) 
        
    precios = [resultado[i][0] for i in range(len(resultado))]
    UODI = [-resultado[i][1] for i in range(len(resultado))]
    Linea_Base = [0 for i in range(len(resultado))]
    EVA = [-resultado[i][3] for i in range(len(resultado))]
    EBITDA = [-resultado[i][2] for i in range(len(resultado))]

    if checkbox_ingresar_valor_negocicion:
        self.grafica_lineas([precios,Linea_Base,EVA,EBITDA],[UODI],["Precios por unidad"],["UODI"],nuevo_precio if nuevo_precio> 1.0 else 0.0)
    else:
        self.grafica_lineas([precios,Linea_Base,EVA,EBITDA],[UODI],["Precios por unidad"],["UODI"])
    
  def mostrar_formulario_1(self,titulo,nombres, formulario1=None, transaccion_internacional=False):
    '''Funcion que genera los formularios para evaluar las oportunidades de inversión, recibe nombre del escenario, lista nombres que
        indica los campos del formulario, formulario1 que es un diccionario que donde se almacena los valores de los campos, si no se pasa por 
        parametro inicializa las variables en 0 y transaccion_internacional que es un booleano que indica si se debe o no añadir la opción de 
        indicar el precio en pesos y trasnformarlo'''
    
    #inicializo variables locales para uso posterior
    costo_dolares=0.0
    checkbox_operacion_dolarizado=False
    st.title(titulo)
    if formulario1 is None:
        #inicializo los valores en 0.0 o vacios si formulario1 no esta declarado
        # formulario1 = {nombre: (0.0 if nombre!= "Incoterm" else "FOB") for nombre in nombres}

        
        if 'Nuevo Escenario'==titulo:
            # este if se utiliza para saber si el nuevo escenario es nacional o internacional
            if transaccion_internacional:
                formulario1={
                    "Cantidad: unidades (unidad determinada por el negociador) a pedir en el periodo de tiempo establecido":30000.0,
                    "Frecuencia: Tiempo (Semanas) estimaddo para recalcular próximo envío":4.0,
                    "Incoterm":"FOB",   
                    "lead time planta-puerto: (Semanas)":5.0,
                    "Semanas cxp: condición de pago tiempo en semanas estimado para pagar a mi proveedor el pedido actual":12.86,
                    "Moq: Cantidad mínima a pedir (en la unidad que se desee manejar)":24000.0,
                    "Adu: Consumo promedio diario (en la unidad que se desee manejar)":23800.0,
                    "Factor lead time: De 0 a 1 qué tan confiable es el lead time, siendo 0 muy seguro y 1 completamente variable":0.1,
                    "Factor variación: De 0 a 1 qué tan confiable es el consumo, siendo 0 muy seguro y 1 completamente variable":0.3,
                    "Estandar posición: Unidades por estiba":350.0,
                    "lead time tiempo-admon: (Semanas)":10.0,
                    "lead time puerto-puerto: (Semanas)":8.0,
                    "lead time gestión cargo: (Semanas)":2.0,
                    "lead time gz-planta: (Semanas)":1.0,
                    "Factor de importacion":0.0,
                    "Tarifa almacenamiento por unidad de consumo":15.0,
                    "Flete internacional: por unidad":0.0,
                    "Arancel: por unidad":0.0,
                    "Costo por servir: por unidad":0.0,
                    "Flete nacional: por unidad":0.0,
                    "Factor de importacion":1.0,
                    "Precio compra: no incluye aranceles":14000.0
                            }
            else:
                formulario1={ "Cantidad: unidades (unidad determinada por el negociador) a pedir en el periodo de tiempo establecido": 30000.0,
                        "Frecuencia: Tiempo (Semanas) estimaddo para recalcular próximo envío":1.0,
                        "lead time entrega en planta: (Semanas)":1.0,
                        "Semanas cxp: condición de pago tiempo en semanas estimado para pagar a mi proveedor el pedido actual":8.57,
                        "Moq: Cantidad mínima a pedir (en la unidad que se desee manejar)":1200.0,
                        "Adu: Consumo promedio diario (en la unidad que se desee manejar)":20890.0,
                        "Factor lead time: De 0 a 1 qué tan confiable es el lead time, siendo 0 muy seguro y 1 completamente variable":0.4,
                        "Factor variación: De 0 a 1 qué tan confiable es el consumo, siendo 0 muy seguro y 1 completamente variable":0.3,
                        "Estandar posición: Unidades por estiba":350.0,
                        "Tarifa almacenamiento por unidad de consumo":15.0
                        }

        else:
            formulario1={
            "Cantidad: unidades (unidad determinada por el negociador) a pedir en el periodo de tiempo establecido":30000.0,
            "Frecuencia: Tiempo (Semanas) estimaddo para recalcular próximo envío":4.0,
            "Incoterm":"FOB",   
            "lead time planta-puerto: (Semanas)":5.0,
            "Semanas cxp: condición de pago tiempo en semanas estimado para pagar a mi proveedor el pedido actual":12.86,
            "Moq: Cantidad mínima a pedir (en la unidad que se desee manejar)":24000.0,
            "Adu: Consumo promedio diario (en la unidad que se desee manejar)":23800.0,
            "Factor lead time: De 0 a 1 qué tan confiable es el lead time, siendo 0 muy seguro y 1 completamente variable":0.1,
            "Factor variación: De 0 a 1 qué tan confiable es el consumo, siendo 0 muy seguro y 1 completamente variable":0.3,
            "Estandar posición: Unidades por estiba":350.0,
            "lead time tiempo-admon: (Semanas)":10.0,
            "lead time puerto-puerto: (Semanas)":8.0,
            "lead time gestión cargo: (Semanas)":2.0,
            "lead time gz-planta: (Semanas)":1.0,
            "Factor de importacion":0.0,
            "Tarifa almacenamiento por unidad de consumo":15.0,
            "Flete internacional: por unidad":0.0,
            "Arancel: por unidad":0.0,
            "Costo por servir: por unidad":0.0,
            "Flete nacional: por unidad":0.0,
            "Factor de importacion":1.0,
            "Precio compra: no incluye aranceles":14000.0
            }
    
    #indico que mostrare la informacion en 2 columnas e inicializo variable local valores que es donde voy a guardadr temporalmente las respuestas
    col1_1, col1_2 = st.columns(2)
    valores = []
    opcion_iconterm="FOB"
    importacion=0.0
    
    with col1_1:
        for i in range(int(len(nombres)/2)):
            if "Incoterm"==nombres[i]:              
                opciones = ["FOB", "COSTO Y FLETE", "EXWORK"]
                # Muestra una lista desplegable
                valores.append(st.selectbox("Selecciona un Incoterm:", opciones,index=opciones.index(formulario1[nombres[i]]), key="Incoterm"))
                opcion_iconterm=valores[-1]
            else:    
                valores.append(st.number_input(nombres[i], step=0.1, min_value=0.0, max_value=10000000.0, value=formulario1[nombres[i]]))
        
        if transaccion_internacional==True:
            #genero proceso extra para transformar de dolares a pesos y pesos a dolares
            checkbox_operacion_dolarizado = st.checkbox("indicar el precio en dolares")
            if checkbox_operacion_dolarizado:
#                 si se selecciono el checkbox_operacion_dolarizado entonces ingresa y hace la variable 
#                     costo_dolares=session_state.valor_en_pesos(inicializada en el main con valor 0.0)/session_state.trm(inicializada en el main con valor 4.800) 
#                     luego genero un campo para indicar trm al momento de la negociación, igual que el campo para indicar el precio en dolares,
#                     luego hago guardo en la variable de estado valor_en_pesos el valor en pesos de la transaccion indicada
                    
                costo_dolares=self.valor_en_pesos/self.trm
                self.trm=st.number_input("Valor TRM", step=0.1000, min_value=0.0, max_value=100000.0, value=self.trm) 
                costo_dolares=st.number_input("Precio compra en dolares", step=0.001, min_value=0.0, max_value=100000.0, value=costo_dolares) 
                self.valor_en_pesos=costo_dolares*self.trm  
    
    with col1_2:
#         '''Si la transaccion no es dolarizada se traen todos los campos del formulario y ya'''
        if transaccion_internacional  and not('Nuevo Escenario'==titulo):
            for i in range(int(len(nombres)/2), len(nombres)-6):                              
                valores.append(st.number_input(nombres[i],key=nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))
            #Genero validacion para el iconterm, reconocer en que valores aplica todos los campos y cuando no
            if  opcion_iconterm == "EXWORK" or importacion!=0.0: 
                for i in range(len(nombres)-6, len(nombres)-2):                              
                    valores.append(st.number_input(nombres[i],key=nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=0.0,disabled=True))
            else:
                for i in range(len(nombres)-6, len(nombres)-2):                              
                    valores.append(st.number_input(nombres[i],key=nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))    
                #si los otros valores son myores a 0 esto se habce igual a 0
            if not (valores[-6]>0.0 or valores[-5]>0.0 or valores[-4]>0.0 or valores[-3]>0.0):
                valores.append(st.number_input(nombres[-2],key=nombres[-2], step=0.1, min_value=0.0, max_value=100000.0, value=1.0, disable=True))            
            else:    
                valores.append(st.number_input(nombres[-2],key=nombres[-2], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[-2]]))            
            importacion=valores[-2]
            if not checkbox_operacion_dolarizado:
#                 Si no se ha seleccionado la alternativa de operacion dolarizda indico que el valor de la ultima variable puesta en nombre es lo que esta
#                     en la variable de estado valor_en_pesos(inicializada en el main con valor 0.0 y modificada cuando selecciono la operacion dolarizada
#                     y llevo a valor_en_pesos el valor que se escriba en este campo)
                valores.append(st.number_input(nombres[-1],key=nombres[-1], step=0.1, min_value=0.0, max_value=10000000.0, value=self.valor_en_pesos))
                self.valor_en_pesos=valores[-1]
            else:            
                #traigo valor_en_pesos pero no permito su edicion
                valores.append(st.number_input(nombres[-1],key=nombres[-1], step=0.1, min_value=0.0, max_value=10000000.0, value=self.valor_en_pesos,disabled=True))
        else:
            for i in range(int(len(nombres)/2), len(nombres)):
                valores.append(st.number_input(nombres[i],key=nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))

          
    if st.button("Guardar"): 
        if 0.0 == valores[-1]:
            self.error=True
            st.error("hay un dato con valor 0.0 o vacio")
        else:
            if transaccion_internacional and not('Nuevo Escenario'==titulo):
                valores[-1]=self.valor_en_pesos
            formulario1 = {nombre: valores[index] for index, nombre in enumerate(nombres)}
            self.error=False
            st.success(f"Datos guardados correctamente ")
      
    return formulario1,self.valor_en_pesos,self.error,self.trm
          
  def grafica_lineas(self,eje_x,eje_y,titulo_x,titulo_y,nuevo_precio=0.0):         
    precios=eje_x[0]
    linea_base=eje_x[1]
    EVA=eje_x[2]
    EBITDA=eje_x[3]
    UODI=eje_y[0] 
    
#     Resultado_Compras = Resultado[Resultado['Variable']=="Compra"]
#     Resultado_Inventario = Resultado[Resultado['Variable']=="Inventario"]
#     Resultado_CostoTotal = Resultado[Resultado['Variable']=="CostoTotal"]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

#     fig.add_trace(go.Scatter(x=precios, y=UODI, name='Compras'))

    fig.add_trace(go.Scatter(x=precios, y=UODI, 
                             name='UODI', mode='lines', line=dict(color='green'), legendrank=True))
  
    fig.add_trace(go.Scatter(x=precios, y=EVA, 
                             name='EVA', mode='lines', line=dict(color='Orange'), legendrank=True))
  
    fig.add_trace(go.Scatter(x=precios, y=EBITDA, 
                             name='EBITDA', mode='lines', line=dict(color='Red'), legendrank=True))
    
    fig.add_trace(go.Scatter(x=precios, y=linea_base, 
                             name='linea base', mode='lines', line=dict(color='Yellow'), legendrank=True))

#     fig.add_trace(go.Scatter(x=Resultado_Compras['Semana'], y=Resultado_Compras['Precios'], 
#                              name='Precios', mode='lines', line=dict(color='orange'), legendrank=True), secondary_y=True)
    if nuevo_precio>0:
        fig.add_shape(
            type="line",
            x0=nuevo_precio, y0=min(UODI), x1=nuevo_precio, y1=max(UODI),
            line=dict(color="blue", width=2, dash="dash"),
        )

    fig.update_layout(title='Variación de indicadores financieros en funcion del precio',
                      xaxis=dict(title='Precios'),
                      yaxis=dict(title='Valor'),
#                       yaxis2=dict(title='Precios', overlaying='y', side='right'),
                     legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ))

    st.write(fig)

