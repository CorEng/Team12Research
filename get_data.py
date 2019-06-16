import pandas as pd

df_stops = pd.ExcelFile("dublinbusstops.xls")
df = df_stops.parse("Sheet1")

df["Latitude"] = None
df["Longitude"] = None




for i, value in enumerate(df["Coordinates"]):

    if type(df["Coordinates"][i]) != float:
        df.at[i, "Latitude"] = df["Coordinates"][i][7:13]
        df.at[i, "Longitude"] = df["Coordinates"][i][15:]
    else:
        continue

df = df.dropna()
df = df.drop(["Unique British Isles Id", "Map", "Coordinates", "Projection", "Easting", "Prov", "Unnamed: 9",
              "Northing"], axis = 1)

print(df.tail())

with pd.ExcelWriter('final_stops.xls') as writer:
    df.to_excel(writer)

