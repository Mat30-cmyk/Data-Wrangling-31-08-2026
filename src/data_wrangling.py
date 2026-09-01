# =============================================================================
# DATA WRANGLING - DataAnalytics Colombia S.A.S.
# Sesion 5: Limpieza, preparacion y filtrado de datos con Pandas
#
# Programa completo que:
#   Fase 1 -> diagnostica la calidad de los datos originales.
#   Fase 2 -> explica los problemas encontrados.
#   Fase 3 -> limpia y normaliza los datos.
#   Fase 4 -> aplica filtros condicionales simples y multiples.
#   Fase 5 -> aplica una segmentacion obligatoria usando isin().
#   Fase 6 -> genera 5 segmentos comerciales.
#   Fase 7 -> exporta los resultados a CSV y a Excel (varias hojas).
#
# REGLA DE ORO DEL PROYECTO:
#   El archivo original (Data/clientes_originales_data_wrangling.csv) NUNCA
#   se sobrescribe. Todo el trabajo se hace sobre una COPIA en memoria
#   (el DataFrame de Pandas). Los resultados se guardan en archivos nuevos
#   dentro de la carpeta Reports/.
# =============================================================================

import os
import pandas as pd


# -----------------------------------------------------------------------------
# Rutas de archivos
# -----------------------------------------------------------------------------

CARPETA_SRC = os.path.dirname(os.path.abspath(__file__))
CARPETA_PROYECTO = os.path.dirname(CARPETA_SRC)

RUTA_DATOS_ORIGINALES = os.path.join(
    CARPETA_PROYECTO,
    "Data",
    "clientes_originales_data_wrangling.csv"
)

CARPETA_REPORTS = os.path.join(CARPETA_PROYECTO, "Reports")

RUTA_CLIENTES_LIMPIOS = os.path.join(
    CARPETA_REPORTS,
    "clientes_limpios.csv"
)

RUTA_REPORTE_EXCEL = os.path.join(
    CARPETA_REPORTS,
    "reporte_segmentacion.xlsx"
)


# -----------------------------------------------------------------------------
# Columnas de texto
# -----------------------------------------------------------------------------

COLUMNAS_TEXTO = [
    "Nombre",
    "Ciudad",
    "Genero",
    "Categoria",
    "Estado"
]


# -----------------------------------------------------------------------------
# Diccionarios de normalizacion
# -----------------------------------------------------------------------------

MAPA_CIUDADES = {
    "MEDELLIN": "Medellín",
    "MEDELLÍN": "Medellín",
    "CALI": "Cali",
    "BOGOTA": "Bogotá",
    "BOGOTÁ": "Bogotá",
    "QUIBDO": "Quibdó",
    "QUIBDÓ": "Quibdó",
    "CARTAGENA": "Cartagena",
    "BARRANQUILLA": "Barranquilla",
}


MAPA_GENERO = {
    "M": "Masculino",
    "MASCULINO": "Masculino",
    "HOMBRE": "Masculino",
    "F": "Femenino",
    "FEMENINO": "Femenino",
    "MUJER": "Femenino",
}


MAPA_CATEGORIA = {
    "BASICA": "Básica",
    "BÁSICA": "Básica",
    "CORPORATIVO": "Corporativo",
    "ESTANDAR": "Estándar",
    "ESTÁNDAR": "Estándar",
    "PREMIUM": "Premium",
}


MAPA_ESTADO = {
    "ACTIVO": "Activo",
    "INACTIVO": "Inactivo",
}


# =============================================================================
# FASE 1 - CARGA Y DIAGNOSTICO
# =============================================================================

def cargar_datos(ruta: str) -> pd.DataFrame:
    """
    Carga el CSV original en un DataFrame.
    El archivo original nunca se modifica.
    """
    df = pd.read_csv(ruta)
    return df


def diagnostico(df: pd.DataFrame, titulo: str) -> None:
    """
    Imprime un diagnostico de calidad de los datos.
    """

    print("=" * 70)
    print(titulo)
    print("=" * 70)

    filas, columnas = df.shape

    print(f"\nCantidad total de registros: {filas}")
    print(f"Cantidad de columnas: {columnas}")

    print("\nNombres de las columnas:")
    print(list(df.columns))

    print("\nTipos de datos por columna:")
    print(df.dtypes)

    print("\nPrimeros 5 registros:")
    print(df.head())

    print("\nUltimos 5 registros:")
    print(df.tail())

    print("\nCantidad de valores nulos por columna:")
    print(df.isnull().sum())

    print(
        f"\nCantidad de registros duplicados: "
        f"{df.duplicated().sum()}"
    )

    print("\nValores unicos de Ciudad:")
    print(sorted(df["Ciudad"].dropna().unique()))

    print("\nValores unicos de Genero:")
    print(sorted(df["Genero"].dropna().unique()))

    print("\nValores unicos de Categoria:")
    print(sorted(df["Categoria"].dropna().unique()))

    print("\nValores unicos de Estado:")
    print(sorted(df["Estado"].dropna().unique()))

    print(
        f"\nEdad minima: {df['Edad'].min()}  /  "
        f"Edad maxima: {df['Edad'].max()}"
    )

    print(
        f"ValorCompra minimo: {df['ValorCompra'].min()}  /  "
        f"ValorCompra maximo: {df['ValorCompra'].max()}"
    )

    print()


# =============================================================================
# FASE 3 - LIMPIEZA Y PREPARACION
# =============================================================================

def quitar_espacios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Elimina espacios sobrantes al inicio y al final
    de las columnas de texto.
    """

    for columna in COLUMNAS_TEXTO:
        df[columna] = df[columna].str.strip()

    return df


def normalizar_columna(
    serie: pd.Series,
    mapa: dict
) -> pd.Series:
    """
    Normaliza una columna de texto usando un diccionario.
    """

    en_mayusculas = serie.str.upper()
    normalizada = en_mayusculas.replace(mapa)

    return normalizada


def tratar_edades_invalidas(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Corrige edades menores de 18 o mayores de 100
    utilizando la mediana de las edades validas.
    """

    mascara_invalida = (
        (df["Edad"] < 18) |
        (df["Edad"] > 100)
    )

    mediana_edad = df.loc[
        ~mascara_invalida,
        "Edad"
    ].median()

    print(
        f"Edades invalidas detectadas y corregidas: "
        f"{mascara_invalida.sum()} "
        f"(se reemplazaron por la mediana = {mediana_edad})"
    )

    df.loc[
        mascara_invalida,
        "Edad"
    ] = mediana_edad

    return df


def tratar_compras_invalidas(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Corrige valores negativos de ValorCompra
    utilizando su valor absoluto.
    """

    mascara_negativos = df["ValorCompra"] < 0

    print(
        f"Compras con valor negativo corregidas: "
        f"{mascara_negativos.sum()}"
    )

    df.loc[
        mascara_negativos,
        "ValorCompra"
    ] = df.loc[
        mascara_negativos,
        "ValorCompra"
    ].abs()

    return df


def tratar_nulos(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Rellena los valores nulos.

    Columnas numericas:
        Se utiliza la mediana.

    Columnas categoricas:
        Se utiliza la etiqueta 'Desconocido'.
    """

    mediana_edad = df["Edad"].median()
    mediana_valor_compra = df["ValorCompra"].median()

    df["Edad"] = df["Edad"].fillna(mediana_edad)
    df["ValorCompra"] = df[
        "ValorCompra"
    ].fillna(mediana_valor_compra)

    for columna in [
        "Ciudad",
        "Genero",
        "Categoria",
        "Estado"
    ]:
        df[columna] = df[columna].fillna(
            "Desconocido"
        )

    return df


def limpiar_datos(
    df_original: pd.DataFrame
) -> pd.DataFrame:
    """
    Funcion principal de limpieza.

    Trabaja sobre una copia del DataFrame original.
    """

    df = df_original.copy()

    # 1. Eliminar duplicados
    duplicados_antes = df.duplicated().sum()

    df = df.drop_duplicates()

    print(
        f"Registros duplicados eliminados: "
        f"{duplicados_antes}"
    )

    # 2. Quitar espacios
    df = quitar_espacios(df)

    # 3. Normalizar columnas categoricas
    df["Ciudad"] = normalizar_columna(
        df["Ciudad"],
        MAPA_CIUDADES
    )

    df["Genero"] = normalizar_columna(
        df["Genero"],
        MAPA_GENERO
    )

    df["Categoria"] = normalizar_columna(
        df["Categoria"],
        MAPA_CATEGORIA
    )

    df["Estado"] = normalizar_columna(
        df["Estado"],
        MAPA_ESTADO
    )

    # 4. Tratar datos invalidos
    df = tratar_edades_invalidas(df)
    df = tratar_compras_invalidas(df)

    # 5. Tratar valores nulos
    df = tratar_nulos(df)

    # 6. Ajustar tipos de datos
    df["Edad"] = df["Edad"].astype(int)

    # 7. Registrar compras iguales a cero
    compras_en_cero = (
        df["Compras"] == 0
    ).sum()

    print(
        "Clientes con 0 compras "
        f"(se conservan, es un dato valido): "
        f"{compras_en_cero}"
    )

    # 8. Verificacion final
    filas_antes_dropna = len(df)

    df = df.dropna()

    filas_eliminadas_por_seguridad = (
        filas_antes_dropna - len(df)
    )

    if filas_eliminadas_por_seguridad > 0:
        print(
            "Filas eliminadas por seguridad "
            f"(nulos no cubiertos): "
            f"{filas_eliminadas_por_seguridad}"
        )

    # 9. Reiniciar indices
    df = df.reset_index(drop=True)

    return df


# =============================================================================
# FASE 4 - FILTROS CONDICIONALES
# =============================================================================

def aplicar_filtros(
    df: pd.DataFrame
) -> None:
    """
    Aplica los 6 filtros condicionales de la actividad.
    """

    print("=" * 70)
    print("FASE 4 - FILTROS CONDICIONALES")
    print("=" * 70)

    # Filtro 1 - Mayores de edad
    filtro_1 = df[df["Edad"] >= 18]

    print(
        f"\nFiltro 1 - Mayores de edad: "
        f"{len(filtro_1)} clientes"
    )

    # Filtro 2 - Clientes de Medellin
    filtro_2 = df[
        df["Ciudad"] == "Medellín"
    ]

    print(
        f"Filtro 2 - Clientes de Medellín: "
        f"{len(filtro_2)} clientes"
    )

    # Filtro 3 - Clientes de alto valor
    filtro_3 = df[
        df["ValorCompra"] > 3_000_000
    ]

    print(
        "Filtro 3 - ValorCompra > 3.000.000: "
        f"{len(filtro_3)} clientes"
    )

    # Filtro 4 - Medellin y mayores de 25
    filtro_4 = df[
        (df["Edad"] > 25) &
        (df["Ciudad"] == "Medellín")
    ]

    print(
        "Filtro 4 - Medellín y mayores de 25 años: "
        f"{len(filtro_4)} clientes"
    )

    # Filtro 5 - Medellin o Cali
    filtro_5 = df[
        (df["Ciudad"] == "Medellín") |
        (df["Ciudad"] == "Cali")
    ]

    print(
        "Filtro 5 - Medellín o Cali: "
        f"{len(filtro_5)} clientes"
    )

    # Filtro 6 - No son de Bogota
    filtro_6 = df[
        ~(df["Ciudad"] == "Bogotá")
    ]

    print(
        "Filtro 6 - Clientes que NO son de Bogotá: "
        f"{len(filtro_6)} clientes"
    )

    print()


# =============================================================================
# FASE 5 - USO OBLIGATORIO DE isin()
# =============================================================================

def segmento_isin(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Selecciona clientes de Medellin, Cali,
    Bogota o Quibdo usando isin().
    """

    ciudades_objetivo = [
        "Medellín",
        "Cali",
        "Bogotá",
        "Quibdó"
    ]

    segmento = df[
        df["Ciudad"].isin(ciudades_objetivo)
    ]

    print("=" * 70)
    print("FASE 5 - SEGMENTO CON isin()")
    print("=" * 70)

    print(
        f"\nClientes en {ciudades_objetivo}: "
        f"{len(segmento)} de {len(df)} "
        "clientes totales\n"
    )

    return segmento


# =============================================================================
# FASE 6 - SEGMENTACION COMERCIAL
# =============================================================================

def segmentos_comerciales(
    df: pd.DataFrame
) -> dict:
    """
    Genera los 5 segmentos comerciales
    pedidos en la actividad.
    """

    print("=" * 70)
    print("FASE 6 - SEGMENTACION COMERCIAL")
    print("=" * 70)

    # Segmento A - Clientes premium
    segmento_premium = df[
        df["ValorCompra"] > 5_000_000
    ]

    # Segmento B - Clientes jovenes
    segmento_joven = df[
        df["Edad"].between(18, 25)
    ]

    # Segmento C - Ciudades principales
    segmento_ciudades_principales = df[
        df["Ciudad"].isin([
            "Medellín",
            "Cali",
            "Bogotá"
        ])
    ]

    # Segmento D - Clientes activos
    segmento_activos = df[
        ~(df["Estado"] == "Inactivo")
    ]

    # Segmento E - Clientes de alto potencial
    segmento_alto_potencial = df.query(
        "Edad >= 25 and Edad <= 50 and "
        "Compras > 5 and "
        "ValorCompra > 2000000 and "
        "Estado == 'Activo'"
    )

    segmentos = {
        "Segmento_Premium": segmento_premium,
        "Segmento_Joven": segmento_joven,
        "Ciudades_Principales":
            segmento_ciudades_principales,
        "Clientes_Activos": segmento_activos,
        "Alto_Potencial":
            segmento_alto_potencial,
    }

    for nombre, segmento_df in segmentos.items():
        print(
            f"{nombre}: "
            f"{len(segmento_df)} clientes"
        )

    print()

    return segmentos


# =============================================================================
# FASE 7 - GENERACION DE RESULTADOS
# =============================================================================

def exportar_resultados(
    df_limpio: pd.DataFrame,
    segmentos: dict
) -> None:
    """
    Exporta el dataset limpio a CSV y genera
    un reporte Excel con varias hojas.
    """

    print("=" * 70)
    print("FASE 7 - EXPORTACION DE RESULTADOS")
    print("=" * 70)

    # Crear carpeta Reports
    os.makedirs(
        CARPETA_REPORTS,
        exist_ok=True
    )

    # CSV con datos limpios
    df_limpio.to_csv(
        RUTA_CLIENTES_LIMPIOS,
        index=False
    )

    print(
        f"\nArchivo generado: "
        f"{RUTA_CLIENTES_LIMPIOS}"
    )

    # Excel con varias hojas
    with pd.ExcelWriter(
        RUTA_REPORTE_EXCEL,
        engine="openpyxl"
    ) as writer:

        # Datos limpios
        df_limpio.to_excel(
            writer,
            sheet_name="Datos_Limpios",
            index=False
        )

        # Segmentos
        for nombre_hoja, segmento_df in segmentos.items():
            segmento_df.to_excel(
                writer,
                sheet_name=nombre_hoja,
                index=False
            )

        # Hoja de resumen
        resumen = pd.DataFrame(
            {
                "Segmento": list(
                    segmentos.keys()
                ),
                "Cantidad_Clientes": [
                    len(df)
                    for df in segmentos.values()
                ]
            }
        )

        resumen.to_excel(
            writer,
            sheet_name="Resumen",
            index=False
        )

    print(
        f"Archivo generado: "
        f"{RUTA_REPORTE_EXCEL}"
    )

    print()


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================

def main():

    # Fase 1
    df_original = cargar_datos(
        RUTA_DATOS_ORIGINALES
    )

    diagnostico(
        df_original,
        "FASE 1 - DIAGNOSTICO INICIAL "
        "(DATOS ORIGINALES)"
    )

    # Fase 3
    df_limpio = limpiar_datos(
        df_original
    )

    # Verificacion despues de la limpieza
    diagnostico(
        df_limpio,
        "DIAGNOSTICO POSTERIOR "
        "A LA LIMPIEZA"
    )

    # Fase 4
    aplicar_filtros(df_limpio)

    # Fase 5
    segmento_isin(df_limpio)

    # Fase 6
    segmentos = segmentos_comerciales(
        df_limpio
    )

    # Fase 7
    exportar_resultados(
        df_limpio,
        segmentos
    )

    print(
        "Proceso de Data Wrangling "
        "finalizado con exito."
    )


if __name__ == "__main__":
    main()