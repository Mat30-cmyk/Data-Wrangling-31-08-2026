import pandas as pd

ruta = "../data/clientes_originales_data_wrangling.csv"

df = pd.read_csv(ruta)

print(df.head())