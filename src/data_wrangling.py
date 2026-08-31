# =============================================================================
# DATA WRANGLING - DataAnalytics Colombia S.A.S.
# Sesion 5: Limpieza, preparacion y filtrado de datos con Pandas
#
# Este es un avance del proyecto (Fase 1). En este punto el programa solo
# CARGA el archivo original y realiza un DIAGNOSTICO de calidad de los datos.
# Todavia no se realiza ninguna limpieza: el objetivo de esta fase es
# entender que problemas tiene el dataset antes de tocarlo.
#
# IMPORTANTE: el archivo original (Data/clientes_originales_data_wrangling.csv)
# nunca se modifica. Siempre se trabaja sobre el DataFrame que Pandas carga en
# memoria (una "copia" de los datos), nunca se escribe sobre el CSV original.
# =============================================================================

import pandas as pd

# Ruta relativa desde la carpeta src/ hacia la carpeta Data/
# Se usa os.path mas adelante en el proyecto para que la ruta funcione sin
# importar desde donde se ejecute el script; por ahora usamos ruta relativa
# simple porque el script se ejecuta desde la carpeta src/.
RUTA_DATOS_ORIGINALES = "../Data/clientes_originales_data_wrangling.csv"


def cargar_datos(ruta: str) -> pd.DataFrame:
    """
    Carga el archivo CSV original en un DataFrame de Pandas.

    Parametros
    ----------
    ruta : str
        Ruta del archivo CSV a cargar.

    Retorna
    -------
    pd.DataFrame
        DataFrame con los datos cargados en memoria (el CSV original no se
        toca ni se sobrescribe en ningun momento).
    """
    df = pd.read_csv(ruta)
    return df


def diagnostico_inicial(df: pd.DataFrame) -> None:
    """
    Muestra en consola un diagnostico basico de calidad de los datos.

    Esta funcion corresponde a la Fase 1 del reto: no modifica el DataFrame,
    solo IMPRIME informacion para que el equipo pueda identificar problemas
    (nulos, duplicados, valores inconsistentes, rangos invalidos, etc.).
    """
    print("=" * 70)
    print("FASE 1 - DIAGNOSTICO INICIAL DE LOS DATOS")
    print("=" * 70)

    # --- Tamano del dataset -------------------------------------------------
    cantidad_registros, cantidad_columnas = df.shape
    print(f"\nCantidad total de registros: {cantidad_registros}")
    print(f"Cantidad de columnas: {cantidad_columnas}")

    # --- Nombres de columnas y tipos de dato --------------------------------
    print("\nNombres de las columnas:")
    print(list(df.columns))

    print("\nTipos de datos por columna:")
    print(df.dtypes)

    # --- Vista rapida de los datos (head / tail) ----------------------------
    print("\nPrimeros 5 registros:")
    print(df.head())

    print("\nUltimos 5 registros:")
    print(df.tail())

    # --- Valores nulos -------------------------------------------------------
    # isnull().sum() cuenta, por columna, cuantas celdas estan vacias (NaN).
    print("\nCantidad de valores nulos por columna:")
    print(df.isnull().sum())

    # --- Registros duplicados -------------------------------------------------
    # duplicated() marca True en las filas que son una copia exacta de otra
    # fila anterior. sum() cuenta cuantos True hay.
    print(f"\nCantidad de registros duplicados: {df.duplicated().sum()}")

    # --- Valores unicos en columnas categoricas -------------------------------
    # unique() nos permite ver TODAS las variantes con las que aparece un
    # mismo dato (ej: 'Medellin', 'medellin', 'MEDELLIN', 'Medellín').
    # Esto es clave para detectar inconsistencias de escritura.
    print("\nValores unicos de Ciudad:")
    print(df["Ciudad"].unique())

    print("\nValores unicos de Genero:")
    print(df["Genero"].unique())

    print("\nValores unicos de Categoria:")
    print(df["Categoria"].unique())

    print("\nValores unicos de Estado:")
    print(df["Estado"].unique())

    # --- Rangos de columnas numericas -----------------------------------------
    # min()/max() nos ayudan a detectar valores fuera de rango logico, por
    # ejemplo edades negativas o mayores a 100 anios.
    print(f"\nEdad minima: {df['Edad'].min()}  /  Edad maxima: {df['Edad'].max()}")
    print(
        f"ValorCompra minimo: {df['ValorCompra'].min()}  /  "
        f"ValorCompra maximo: {df['ValorCompra'].max()}"
    )

    print("\n" + "=" * 70)
    print("FIN DEL DIAGNOSTICO INICIAL")
    print("=" * 70)


def main():
    """Punto de entrada del script (avance Fase 1)."""
    df_original = cargar_datos(RUTA_DATOS_ORIGINALES)
    diagnostico_inicial(df_original)

if __name__ == "__main__":
    main()
