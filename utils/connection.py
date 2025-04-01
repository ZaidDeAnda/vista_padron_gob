import pandas as pd
import json

import psycopg2
import streamlit as st

def connect():
    with open('creds.json') as f:
        params= json.load(f)
    connection = psycopg2.connect(**params)

    return connection

def read_data_from_sql(connection):
    query = '''SELECT t1.persona_id,
                t2."CURP",
                t2.nombres,
                t2.ap_materno,
                t2.fecha_nacimiento,
                t2.estado_nacimiento,
                t3.estatus,
                t4.nombre,
                t4.programa,
                t4.dependencia
                FROM "PersonasOnTramites" t1
                LEFT JOIN "Persona" t2 ON t2.id = t1.persona_id
                LEFT JOIN "Tramite" t3 ON t3.id = t1.tramite_id
                LEFT JOIN "ProcesoPrograma" t4 ON t4.id = t3.proceso_id LIMIT 500;'''

    data = pd.read_sql_query(query,connection)

    return data

def read_complete_data_from_sql(connection):
    query = '''SELECT t1.persona_id,
                t2."CURP",
                t2.nombres,
                t2.ap_materno,
                t2.fecha_nacimiento,
                t2.estado_nacimiento,
                t3.estatus,
                t4.nombre,
                t4.programa,
                t4.dependencia,
                t5.*,
                t6.*,
                t7.*

                FROM "PersonasOnTramites" t1
                LEFT JOIN "Persona" t2 ON t2.id = t1.persona_id
                LEFT JOIN "Tramite" t3 ON t3.id = t1.tramite_id
                LEFT JOIN "ProcesoPrograma" t4 ON t4.id = t3.proceso_id
                LEFT JOIN "CaracteristicaSociodemograficaPersona" t5 ON t5.persona_id = t1.persona_id
                LEFT JOIN "CaracteristicaSocioeconomicaPersona" t6 ON t6.persona_id = t1.persona_id
                LEFT JOIN "SaludPersona" t7 ON t7.persona_id = t1.persona_id;'''

    data = pd.read_sql_query(query,connection)

    return data







