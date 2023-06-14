import streamlit as st
from streamlit import session_state
import matplotlib.pyplot as plt
import mplcursors

class streamlit_frm:
  def __init__(self,valor_en_pesos,trm=4800.00):
        self.error=True
        self.trm=trm
        self.valor_en_pesos=valor_en_pesos 
   
  def resultados(self,resultado):
    st.write(f"El precio maximo a pagar es: {resultado[0][0]}")
    st.write("implica una variación de {:.2f}%".format((resultado[0][0]-self.valor_en_pesos)/self.valor_en_pesos*100))    
    st.write(f"UODI: {resultado[0][1]}")
    st.write(f"EBITDA: {resultado[0][2]}")
    st.write(f"EVA: {resultado[0][3]}")
    st.write(f"ROIC: {0 if resultado[0][4] == 0 else resultado[0][1]/resultado[0][4]}")
    
    precios = [resultado[i][0] for i in range(len(resultado))]
    UODI = [resultado[i][1] for i in range(len(resultado))]
    Linea_Base = [0 for i in range(len(resultado))]
    st.write(precios,UODI)
    self.grafica_lineas([precios,Linea_Base],[UODI],["Precios por unidad"],["UODI"])
    
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
        formulario1 = {nombre: (0.0 if nombre!= "Incoterm" else "") for nombre in nombres}
    
    #indico que mostrare la informacion en 2 columnas e inicializo variable local valores que es donde voy a guardadr temporalmente las respuestas
    col1_1, col1_2 = st.columns(2)
    valores = []
    
    with col1_1:
        for i in range(int(len(nombres)/2)):
            if "Incoterm"==nombres[i]:
                valores.append(st.text_input(nombres[i], value=formulario1[nombres[i]]))
            else:    
                valores.append(st.number_input(nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))
        
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
        if transaccion_internacional==True:
            for i in range(int(len(nombres)/2), len(nombres)-1):
                valores.append(st.number_input(nombres[i],key=nombres[i], step=0.1, min_value=0.0, max_value=100000.0, value=formulario1[nombres[i]]))
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
        if 0.0 in valores or "" in valores:
            self.error=True
            st.error("hay un dato con valor 0.0 o vacio")
        else:
            if transaccion_internacional==True:
                valores[-1]=self.valor_en_pesos
            formulario1 = {nombre: valores[index] for index, nombre in enumerate(nombres)}
            self.error=False
            st.success(f"Datos guardados correctamente {valores[-1]}  {self.valor_en_pesos}")
      
    return formulario1,self.valor_en_pesos,self.error,self.trm
  
  def grafica_lineas(self,eje_x,eje_y,titulo_x,titulo_y):
        
    precios=eje_x[0]
    linea_base=eje_x[1]
    UODI=eje_y[0]
    fig, ax = plt.subplots()
    linea1, = ax.plot(precios, linea_base, marker='o', label='Escenario 1')
    linea2, = ax.plot(precios, UODI, marker='o', label='Escenario 1')

    # Configurar los ejes y la leyenda
    ax.set_xlabel('Precios')
    ax.set_ylabel('UODI')
    ax.legend()

    # Configurar los marcadores y las etiquetas al pasar el mouse
    cursor1 = mplcursors.cursor(linea1, hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(f"({sel.target[0]}, {sel.target[1]})"))
    cursor2 = mplcursors.cursor(linea2, hover=True)
    cursor2.connect("add", lambda sel: sel.annotation.set_text(f"({sel.target[0]}, {sel.target[1]})"))

  # Mostrar el gráfico en Streamlit
    st.pyplot(fig)




