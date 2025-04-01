import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import base64
import json

from utils.connection import read_data_from_sql, connect, read_complete_data_from_sql

def drop_missing(df):
    filtered_df = df.loc[df['CURP'].notna()]
    return filtered_df

@st.cache_data
def read_data(user, selection="partial"):
    if selection=="debug":
        data = pd.read_csv('data-integrator-jul26.csv')
    else:
        conn = connect()
        if selection== "partial":
            data = read_data_from_sql(conn)
        elif selection == "complete":
            data = read_complete_data_from_sql(conn)
    filtered_df = drop_missing(data)
    if user == "planeacion":
        filtered_df = filtered_df.loc[filtered_df["nombre"] == "463 - Cuestionario Socioeconomico, CHECS 2023 JAVASCRIPT"]
    return filtered_df

@st.cache_data
def convert_df(df, user, selection):
    if selection == "complete":
        df = read_data(user, selection)
    return df.to_csv().encode('utf-8')

def download_button(object_to_download, download_filename):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    """

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link


def download_df(df, user, selection="partial"):
    csv = convert_df(df, user, selection)
    components.html(
        download_button(csv, "beneficiarios depublicados.csv"),
        height=0,
    )