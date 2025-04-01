import streamlit as st

import pandas as pd

from io import StringIO

from utils.data import read_data, download_df
from utils.authentication import check_password, get_user

#content
col1, col2 = st.columns(2)
#col1.image('auxiliar/sii.png',width=300)
col2.write("## **Secretaria de Igualda e Inclusión**")
st.write('## Registro de Beneficiarios Duplicados')

if check_password():

    user = get_user()

    #Este selection controla que datos se van a mostrar. Partial muestra el query solo con las columnas seleccionadas. Complete muestra TODAS las columnas
    filtered_df = read_data(user, selection="partial")    

    st.subheader("Curps registrados")

    st.dataframe(filtered_df)

    busqueda = st.radio(label="Seleccione tipo de busqueda", options=["Individual", "Grupal"])

    if busqueda == "Individual":

        curp_list = [st.text_input(label="Introduzca el curp a buscar")]

    if busqueda == "Grupal":

        tipo = st.radio(label="Seleccione tipo de entrada", options=["Archivo de texto", "CURP's separados por coma"])

        if tipo == "CURP's separados por coma":

            curps = st.text_input(label="Introduzca los curp a buscar")
            curp_list = curps.split(",")

        if tipo == "Archivo de texto":

            curps_file = st.file_uploader(label="Suba un archivo de texto con los curps")

            if curps_file is not None:

                stringio = StringIO(curps_file.getvalue().decode("utf-8"))
                string_data = stringio.read()
                curp_list = string_data.split("\n")
                curp_list = [curp.strip() for curp in curp_list]


    if st.button("Buscar"):
        
        filtered_df = filtered_df.loc[filtered_df['CURP'].isin(curp_list)]

        st.subheader("Resultados 🔍")
        st.dataframe(filtered_df.dropna(how='all', axis=1))


    with st.form("my_form", clear_on_submit=False):
        #Este selection controla que datos se van a descargar. Partial descarga el query solo con las columnas seleccionadas. Complete descarga TODAS las columnas
        submit = st.form_submit_button("Download dataframe", on_click=download_df, kwargs={"user" : user, "selection" : "complete", "df":filtered_df})