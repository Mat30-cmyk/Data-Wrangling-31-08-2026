# Data Wrangling - Clientes DataAnalytics Colombia S.A.S.

Actividad de Aprendizaje No. 5 - Ciencia de Datos con Python (Módulo ADSO - SENA).

## 1. Objetivo

Diagnosticar, limpiar, transformar y segmentar un conjunto de datos de
clientes utilizando Python y Pandas, aplicando filtros condicionales simples
y múltiples, lógica booleana (`&`, `|`, `~`) y el método `isin()`.

## 2. Situación problema

La empresa DataAnalytics Colombia S.A.S. recibió una base de 123 clientes
proveniente de distintos sistemas, con problemas de calidad: duplicados,
datos faltantes, ciudades escritas de formas distintas, categorías
inconsistentes, edades inválidas y valores de compra negativos. Este
proyecto construye un proceso reproducible de Data Wrangling con Python y
Pandas para dejar la información lista para análisis y campañas comerciales.

## 3. Cómo ejecutar el proyecto

```bash
# 1. Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el script principal (desde la carpeta src/)
cd src
python data_wrangling.py
```

El script imprime en consola todo el diagnóstico y proceso paso a paso, y al
finalizar genera dentro de `Reports/`:

- `clientes_limpios.csv`
- `reporte_segmentacion.xlsx`

El archivo original (`Data/clientes_originales_data_wrangling.csv`) **nunca
se modifica**; todo el proceso se hace sobre una copia en memoria.

## 4. Fase 2 - Problemas de calidad identificados

Al ejecutar el diagnóstico inicial (Fase 1) se detectaron los siguientes
problemas en el archivo original (123 registros):

| Problema | Detalle encontrado |
|---|---|
| Valores nulos | 1 nulo en cada una de las columnas: `Edad`, `Ciudad`, `Genero`, `Categoria`, `ValorCompra`, `Estado`. |
| Registros duplicados | 2 registros totalmente duplicados (ID 13 y 58 aparecen dos veces). |
| Espacios innecesarios | Valores como `"  Cartagena  "`, `" activo "`, `"  Estándar  "`. |
| Ciudades inconsistentes | `Medellín`, `medellin`, `MEDELLIN`, `Medellin` (4 formas de la misma ciudad); lo mismo ocurre con Cali, Bogotá y Quibdó. |
| Género inconsistente | `Masculino`, `masculino`, `M`, `Hombre`; `Femenino`, `femenino`, `F`, `Mujer`, `FEMENINO`. |
| Categoría inconsistente | `Premium`, `premium`, `PREMIUM`; `Estándar`, `estándar`, `Estandar`; `Básica`, `BASICA`, `basica`; `Corporativo`, `CORPORATIVO`. |
| Estado inconsistente | `Activo`, `activo`, `ACTIVO`; `Inactivo`, `inactivo`, `INACTIVO`, con espacios extra. |
| Edades inválidas | 3 registros: edad de 15 años (menor de edad), 104 años (fuera de rango) y -3 años (valor imposible). |
| Compras en cero | 3 registros con `Compras = 0` (se documentan pero **no se eliminan**: un cliente registrado sin compras aún es válido). |
| Valores de compra negativos | 3 registros con `ValorCompra` negativo (ej. -250.000), probablemente un error de digitación en el signo. |

## 5. Fase 3 - Estrategias de limpieza aplicadas

- **Duplicados:** se eliminaron con `drop_duplicates()`, dejando solo la
  primera aparición de cada registro.
- **Espacios:** se eliminaron con `str.strip()` en todas las columnas de
  texto.
- **Normalización de texto (Ciudad, Género, Categoría, Estado):** se pasó el
  texto a mayúsculas con `str.upper()` y luego se mapeó cada variante a su
  forma oficial con `replace()`.
- **Nulos numéricos (`Edad`, `ValorCompra`):** se rellenaron con la
  **mediana** de la columna, porque es una medida robusta que no se
  distorsiona con valores extremos.
- **Nulos categóricos (`Ciudad`, `Genero`, `Categoria`, `Estado`):** se
  rellenaron con la etiqueta `"Desconocido"`, para no perder el registro
  completo sin inventar un dato que no conocemos.
- **Edades inválidas** (`<18` o `>100`): se reemplazaron por la mediana de
  las edades válidas usando `loc[]`.
- **Compras negativas:** se corrigieron con el valor absoluto (`abs()`),
  asumiendo un error de signo en la digitación.
- **Verificación final:** se usó `dropna()` como red de seguridad para
  garantizar que no quedara ningún nulo antes de exportar los resultados.

## 6. Fase 4 y 5 - Filtros y `isin()`

El script implementa los 6 filtros condicionales pedidos (mayores de edad,
clientes de Medellín, clientes de alto valor, combinaciones con `&`, `|` y
`~`), además del segmento obligatorio con `isin()` para clientes de
Medellín, Cali, Bogotá o Quibdó.

## 7. Fase 6 - Segmentos comerciales generados

| Segmento | Condición |
|---|---|
| Segmento_Premium | `ValorCompra > 5.000.000` |
| Segmento_Joven | `Edad` entre 18 y 25 años (`between`) |
| Ciudades_Principales | `Ciudad` en Medellín, Cali o Bogotá (`isin`) |
| Clientes_Activos | `Estado` distinto de `Inactivo` (con `~`) |
| Alto_Potencial | Edad 25-50, más de 5 compras, `ValorCompra > 2.000.000` y `Estado == 'Activo'` (`query`) |

## 8. Fase 7 - Resultados generados

- `Reports/clientes_limpios.csv`: dataset completo después de la limpieza.
- `Reports/reporte_segmentacion.xlsx`: libro de Excel con las hojas
  `Datos_Limpios`, `Segmento_Premium`, `Segmento_Joven`,
  `Ciudades_Principales`, `Clientes_Activos`, `Alto_Potencial` y `Resumen`
  (conteo de clientes por segmento).

## 9. Investigación obligatoria - Métodos adicionales de Pandas

| Método | Qué hace | Sintaxis | Problema que resuelve | Cómo se usó en el proyecto |
|---|---|---|---|---|
| `dropna()` | Elimina filas que tengan al menos un valor nulo. | `df.dropna()` | Garantiza que no queden datos incompletos. | Como verificación final de seguridad, después de tratar todos los nulos conocidos con `fillna()`. |
| `fillna()` | Reemplaza los valores nulos por un valor específico. | `df["col"].fillna(valor)` | Evita perder registros completos por un solo dato faltante. | Para rellenar `Edad`/`ValorCompra` con la mediana y las columnas de texto con `"Desconocido"`. |
| `drop_duplicates()` | Elimina filas exactamente iguales a otra anterior. | `df.drop_duplicates()` | Evita contar dos veces al mismo cliente. | Se aplicó al inicio de la limpieza para quitar los 2 registros duplicados. |
| `replace()` | Reemplaza valores que coinciden con las llaves de un diccionario. | `serie.replace({"A": "B"})` | Unifica distintas formas de escribir el mismo dato. | Para normalizar Ciudad, Género, Categoría y Estado a su forma oficial. |
| `astype()` | Convierte una columna a un tipo de dato específico. | `df["col"].astype(int)` | Corrige el tipo de dato tras limpiar (ej. edades que quedaron en float). | Se aplicó a `Edad` para dejarla como número entero. |
| `str.strip()` | Quita espacios en blanco al inicio/fin de un texto. | `df["col"].str.strip()` | Elimina espacios que hacen que Pandas trate el mismo dato como distinto. | Se aplicó a todas las columnas de texto antes de normalizar. |
| `str.upper()` | Convierte texto a mayúsculas. | `df["col"].str.upper()` | Permite comparar/mapear texto sin importar mayúsculas o minúsculas. | Paso previo a `replace()` para normalizar Ciudad, Género, Categoría y Estado. |
| `between()` | Verifica si un valor numérico está dentro de un rango. | `df["col"].between(a, b)` | Más legible que combinar `>=` y `<=` con `&`. | Para el Segmento_Joven (edad entre 18 y 25). |
| `query()` | Filtra un DataFrame escribiendo la condición como texto. | `df.query("col > 5")` | Facilita leer filtros con varias condiciones combinadas. | Para el Segmento Alto_Potencial (4 condiciones combinadas). |
| `loc[]` | Selecciona/modifica filas y columnas según una condición. | `df.loc[condicion, "col"] = valor` | Permite corregir solo las filas inválidas sin tocar las demás. | Para reemplazar edades y valores de compra inválidos. |

## 10. Estructura del proyecto

```
Data-Wrangling/
├── Data/
│   └── clientes_originales_data_wrangling.csv   (nunca se modifica)
├── src/
│   └── data_wrangling.py
├── Reports/
│   ├── clientes_limpios.csv
│   └── reporte_segmentacion.xlsx
├── README.md
├── requirements.txt
└── .gitignore
```

## 11. Requisitos técnicos

- Python 3.x
- pandas
- openpyxl (necesario para exportar a `.xlsx`)
# Data Wrangling - Clientes DataAnalytics Colombia S.A.S.

Actividad de Aprendizaje No. 5 - Ciencia de Datos con Python (Módulo ADSO - SENA).

## 1. Objetivo

Diagnosticar, limpiar, transformar y segmentar un conjunto de datos de
clientes utilizando Python y Pandas, aplicando filtros condicionales simples
y múltiples, lógica booleana (`&`, `|`, `~`) y el método `isin()`.

## 2. Situación problema

La empresa DataAnalytics Colombia S.A.S. recibió una base de 123 clientes
proveniente de distintos sistemas, con problemas de calidad: duplicados,
datos faltantes, ciudades escritas de formas distintas, categorías
inconsistentes, edades inválidas y valores de compra negativos. Este
proyecto construye un proceso reproducible de Data Wrangling con Python y
Pandas para dejar la información lista para análisis y campañas comerciales.

## 3. Cómo ejecutar el proyecto

```bash
# 1. Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el script principal (desde la carpeta src/)
cd src
python data_wrangling.py
```

El script imprime en consola todo el diagnóstico y proceso paso a paso, y al
finalizar genera dentro de `Reports/`:

- `clientes_limpios.csv`
- `reporte_segmentacion.xlsx`

El archivo original (`Data/clientes_originales_data_wrangling.csv`) **nunca
se modifica**; todo el proceso se hace sobre una copia en memoria.

## 4. Fase 2 - Problemas de calidad identificados

Al ejecutar el diagnóstico inicial (Fase 1) se detectaron los siguientes
problemas en el archivo original (123 registros):

| Problema | Detalle encontrado |
|---|---|
| Valores nulos | 1 nulo en cada una de las columnas: `Edad`, `Ciudad`, `Genero`, `Categoria`, `ValorCompra`, `Estado`. |
| Registros duplicados | 2 registros totalmente duplicados (ID 13 y 58 aparecen dos veces). |
| Espacios innecesarios | Valores como `"  Cartagena  "`, `" activo "`, `"  Estándar  "`. |
| Ciudades inconsistentes | `Medellín`, `medellin`, `MEDELLIN`, `Medellin` (4 formas de la misma ciudad); lo mismo ocurre con Cali, Bogotá y Quibdó. |
| Género inconsistente | `Masculino`, `masculino`, `M`, `Hombre`; `Femenino`, `femenino`, `F`, `Mujer`, `FEMENINO`. |
| Categoría inconsistente | `Premium`, `premium`, `PREMIUM`; `Estándar`, `estándar`, `Estandar`; `Básica`, `BASICA`, `basica`; `Corporativo`, `CORPORATIVO`. |
| Estado inconsistente | `Activo`, `activo`, `ACTIVO`; `Inactivo`, `inactivo`, `INACTIVO`, con espacios extra. |
| Edades inválidas | 3 registros: edad de 15 años (menor de edad), 104 años (fuera de rango) y -3 años (valor imposible). |
| Compras en cero | 3 registros con `Compras = 0` (se documentan pero **no se eliminan**: un cliente registrado sin compras aún es válido). |
| Valores de compra negativos | 3 registros con `ValorCompra` negativo (ej. -250.000), probablemente un error de digitación en el signo. |

## 5. Fase 3 - Estrategias de limpieza aplicadas

- **Duplicados:** se eliminaron con `drop_duplicates()`, dejando solo la
  primera aparición de cada registro.
- **Espacios:** se eliminaron con `str.strip()` en todas las columnas de
  texto.
- **Normalización de texto (Ciudad, Género, Categoría, Estado):** se pasó el
  texto a mayúsculas con `str.upper()` y luego se mapeó cada variante a su
  forma oficial con `replace()`.
- **Nulos numéricos (`Edad`, `ValorCompra`):** se rellenaron con la
  **mediana** de la columna, porque es una medida robusta que no se
  distorsiona con valores extremos.
- **Nulos categóricos (`Ciudad`, `Genero`, `Categoria`, `Estado`):** se
  rellenaron con la etiqueta `"Desconocido"`, para no perder el registro
  completo sin inventar un dato que no conocemos.
- **Edades inválidas** (`<18` o `>100`): se reemplazaron por la mediana de
  las edades válidas usando `loc[]`.
- **Compras negativas:** se corrigieron con el valor absoluto (`abs()`),
  asumiendo un error de signo en la digitación.
- **Verificación final:** se usó `dropna()` como red de seguridad para
  garantizar que no quedara ningún nulo antes de exportar los resultados.

## 6. Fase 4 y 5 - Filtros y `isin()`

El script implementa los 6 filtros condicionales pedidos (mayores de edad,
clientes de Medellín, clientes de alto valor, combinaciones con `&`, `|` y
`~`), además del segmento obligatorio con `isin()` para clientes de
Medellín, Cali, Bogotá o Quibdó.

## 7. Fase 6 - Segmentos comerciales generados

| Segmento | Condición |
|---|---|
| Segmento_Premium | `ValorCompra > 5.000.000` |
| Segmento_Joven | `Edad` entre 18 y 25 años (`between`) |
| Ciudades_Principales | `Ciudad` en Medellín, Cali o Bogotá (`isin`) |
| Clientes_Activos | `Estado` distinto de `Inactivo` (con `~`) |
| Alto_Potencial | Edad 25-50, más de 5 compras, `ValorCompra > 2.000.000` y `Estado == 'Activo'` (`query`) |

## 8. Fase 7 - Resultados generados

- `Reports/clientes_limpios.csv`: dataset completo después de la limpieza.
- `Reports/reporte_segmentacion.xlsx`: libro de Excel con las hojas
  `Datos_Limpios`, `Segmento_Premium`, `Segmento_Joven`,
  `Ciudades_Principales`, `Clientes_Activos`, `Alto_Potencial` y `Resumen`
  (conteo de clientes por segmento).

## 9. Investigación obligatoria - Métodos adicionales de Pandas

| Método | Qué hace | Sintaxis | Problema que resuelve | Cómo se usó en el proyecto |
|---|---|---|---|---|
| `dropna()` | Elimina filas que tengan al menos un valor nulo. | `df.dropna()` | Garantiza que no queden datos incompletos. | Como verificación final de seguridad, después de tratar todos los nulos conocidos con `fillna()`. |
| `fillna()` | Reemplaza los valores nulos por un valor específico. | `df["col"].fillna(valor)` | Evita perder registros completos por un solo dato faltante. | Para rellenar `Edad`/`ValorCompra` con la mediana y las columnas de texto con `"Desconocido"`. |
| `drop_duplicates()` | Elimina filas exactamente iguales a otra anterior. | `df.drop_duplicates()` | Evita contar dos veces al mismo cliente. | Se aplicó al inicio de la limpieza para quitar los 2 registros duplicados. |
| `replace()` | Reemplaza valores que coinciden con las llaves de un diccionario. | `serie.replace({"A": "B"})` | Unifica distintas formas de escribir el mismo dato. | Para normalizar Ciudad, Género, Categoría y Estado a su forma oficial. |
| `astype()` | Convierte una columna a un tipo de dato específico. | `df["col"].astype(int)` | Corrige el tipo de dato tras limpiar (ej. edades que quedaron en float). | Se aplicó a `Edad` para dejarla como número entero. |
| `str.strip()` | Quita espacios en blanco al inicio/fin de un texto. | `df["col"].str.strip()` | Elimina espacios que hacen que Pandas trate el mismo dato como distinto. | Se aplicó a todas las columnas de texto antes de normalizar. |
| `str.upper()` | Convierte texto a mayúsculas. | `df["col"].str.upper()` | Permite comparar/mapear texto sin importar mayúsculas o minúsculas. | Paso previo a `replace()` para normalizar Ciudad, Género, Categoría y Estado. |
| `between()` | Verifica si un valor numérico está dentro de un rango. | `df["col"].between(a, b)` | Más legible que combinar `>=` y `<=` con `&`. | Para el Segmento_Joven (edad entre 18 y 25). |
| `query()` | Filtra un DataFrame escribiendo la condición como texto. | `df.query("col > 5")` | Facilita leer filtros con varias condiciones combinadas. | Para el Segmento Alto_Potencial (4 condiciones combinadas). |
| `loc[]` | Selecciona/modifica filas y columnas según una condición. | `df.loc[condicion, "col"] = valor` | Permite corregir solo las filas inválidas sin tocar las demás. | Para reemplazar edades y valores de compra inválidos. |

## 10. Estructura del proyecto

```
Data-Wrangling/
├── Data/
│   └── clientes_originales_data_wrangling.csv   (nunca se modifica)
├── src/
│   └── data_wrangling.py
├── Reports/
│   ├── clientes_limpios.csv
│   └── reporte_segmentacion.xlsx
├── README.md
├── requirements.txt
└── .gitignore
```

## 11. Requisitos técnicos

- Python 3.x
- pandas
- openpyxl (necesario para exportar a `.xlsx`)
