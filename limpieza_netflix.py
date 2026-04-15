import pandas as pd
df = pd.read_csv("netflix_titles.csv")

#Buscando duplicados
print(f"la cantidad de duplicados es: {df.duplicated().sum()}")
#No se encontraron duplicados

#Ahora vamos con los nulos
print(f"la cantidad de nulos es: {df.isna().sum()}")
#encontramos nulos, voy a ver que se puede eliminar y cuales voy a conservar
#Voy a empezar con los que tinen menos valores nulos

#voy a analisar los 4 nulos de RATING 
print(df[df["rating"].isna()][["title","director","cast","country","date_added","release_year","duration","rating"]])
#no encontre ningun error 

#voy a analisar los 3 nulos en DURATION 
print(df[df["duration"].isna()][["title","director","cast","country","date_added","release_year","rating","duration"]])
#encontre algo raro, la DURATION es nula pero RATING tine valores que deberian estar en DURATION, asique lo voy a corregir

#Creo una copia del csv para modificar
df_clean = df.copy()

#En la fila donde DURATION es nulo, remplazo ese valor por el valor de RATING 
duration_nulo = df["duration"].isna()
df_clean.loc[duration_nulo,"duration"] = df.loc[duration_nulo,"rating"]

#En la fila donde RATING esta mal remplazamos por un nulo
df_clean.loc[duration_nulo,"rating"] = None

#Ahora analisemos los 10 nulos de DATE_ADDED 
print(df[df["date_added"].isna()][["title","director","cast","country","date_added","release_year","rating","duration"]])
#no encontre ningun error 

#veo que entre los datos de DIRECTOR CAST y COUNTRY hay demasiada cantadidad de datos faltantes asique no puedo eliminar todos
#voy a ver en que casos esos 3 coinciden para limpiar un poco
filtro_muchos_nulos = df[["director", "cast", "country"]].isna().all(axis=1) 
print(filtro_muchos_nulos.sum())
#hay 96 filas con los valores de DIRECTOR CAST y COUNTRY nulos al mismo tiempo, voy a eliminar estas filas
df_clean = df_clean.dropna(subset=["director", "cast", "country"], how="all")

#converti los valores DATE ADDED en formato fecha y si no puede convertirlo devuelve NaN
df_clean["date_added"] = df_clean["date_added"].str.strip() #quitando los espacios 
df_clean["date_added"] = pd.to_datetime(df_clean["date_added"], errors="coerce")  
df_clean.isna().sum()
#revisando veo q se incrementaron los nulos asique tocara volver a mirar que paso
#El problema parece ser que hay espacios 
#luego de eliminar los espacios volvemos a tener 10 nulls

#converti los valores RELEASE YEAR en formato numero y si no puede convertirlo devuelve NaN
df_clean["release_year"] = pd.to_numeric(df_clean["release_year"], errors="coerce")  
df_clean.isna().sum()

#ahora vamos a rellenar los datos, las demas filas con datos faltantes no las voy a eliminar solo voy a rellenar por "No Especificado" 
df_clean["director"] = df_clean["director"].fillna("No Especificado")
df_clean["cast"] = df_clean["cast"].fillna("No Especificado")
df_clean["country"] = df_clean["country"].fillna("No Especificado")
df_clean["date_added"] = df_clean["date_added"].fillna("No Especificado")
df_clean["rating"] = df_clean["rating"].fillna("No Especificado")
df_clean.isna().sum()

#eliminando la columna DESCRIPTION ya que no le voy a dar ningun uso
df_clean = df_clean.drop(columns=["description"])

#Creo un nuevo csv sin nulos ni duplicados con RELEASE YEAR y DATE ADDED en formato fecha listo para analisar
df_clean.to_csv("csv_netflix_limpio.csv",index=False) 
