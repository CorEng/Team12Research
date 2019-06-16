import pandas as pd

def get_data():
    """Use dublin bus stop data file to obtain the necessary data and save it on a different smaller file"""

    # Open file
    df_stops = pd.ExcelFile("dublinbusstops.xls")
    df = df_stops.parse("Sheet1")

    # Create new columns
    df["Latitude"] = None
    df["Longitude"] = None

    # Take the lat and lon and put them in the correct columns - only to str types
    for i, value in enumerate(df["Coordinates"]):

        if type(df["Coordinates"][i]) != float:
            df.at[i, "Latitude"] = df["Coordinates"][i][7:13]
            df.at[i, "Longitude"] = df["Coordinates"][i][15:]
        else:
            continue

    # Drop unwanted data
    df = df.dropna()
    df = df.drop(["Unique British Isles Id", "Map", "Coordinates", "Projection", "Easting", "Prov", "Unnamed: 9",
                  "Northing"], axis = 1)

    # Create and write new file
    with pd.ExcelWriter('final_stops.xls') as writer:
        df.to_excel(writer)

