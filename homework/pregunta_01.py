"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import os
from datetime import datetime
import pandas as pd

def normalizar_fecha(fecha_str: str) -> str:
    """
    Recibe una fecha en formato 'dd/mm/aaaa' o 'aaaa/mm/dd' y retorna
    siempre 'dd/mm/aaaa'.
    """
    partes = fecha_str.split("/")
    dia_o_anio, mes, anio_o_dia = partes[0], partes[1], partes[2]

    # Si la primera parte tiene 4 dígitos, asumimos que está en formato 'aaaa/mm/dd'
    if len(dia_o_anio) == 4:
        fecha_corr = "/".join(reversed(partes))
    else:
        fecha_corr = "/".join(partes)

    return fecha_corr

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    ruta_entrada = "files/input/solicitudes_de_credito.csv"
    ruta_salida = "files/output/solicitudes_de_credito.csv"

    df = pd.read_csv(ruta_entrada, sep=";")

    # Eliminar filas completamente vacías
    df = df.dropna()

    # Normalizar a minúsculas
    df["sexo"] = df["sexo"].str.lower()
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower()
    df["idea_negocio"] = df["idea_negocio"].str.lower()
    df["barrio"] = df["barrio"].str.lower()
    df["línea_credito"] = df["línea_credito"].str.lower()

    # Reemplazar '_' y '-' por espacio en algunas columnas de texto
    columnas_con_guiones = ["idea_negocio", "barrio", "línea_credito"]
    for col in columnas_con_guiones:
        df[col] = df[col].str.replace("_", " ", regex=False)
        df[col] = df[col].str.replace("-", " ", regex=False)

    # Corregir formato de fecha
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(normalizar_fecha)

    # Limpiar monto_del_credito quitando espacios, '$' y comas
    caracteres_a_quitar = [" ", "$", ","]
    for simbolo in caracteres_a_quitar:
        df["monto_del_credito"] = df["monto_del_credito"].str.replace(
            simbolo, "", regex=False
        )

    df["monto_del_credito"] = df["monto_del_credito"].astype(float)

    # Eliminar duplicados según las columnas indicadas y luego filas con NaN
    columnas_unicas = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]

    df = df.drop_duplicates(subset=columnas_unicas).dropna()

    # Guardar resultado
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    df.to_csv(ruta_salida, sep=";", index=False)