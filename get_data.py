import csv, re, requests, json, datetime
from passw import *
import pymysql


class Stops:

    def __init__(self):
        pass

    def get_all_stops(self):

        no_ceros = re.compile("[1-9][0-9]*")

        with open('stops.csv', encoding="utf8") as read_file:
            read_csv = csv.reader(read_file, delimiter=",")

            stops = []
            for i, row in enumerate(read_csv):
                if i == 0:
                    continue
                else:
                    stop_no = no_ceros.search(row[3][-6:]).group()
                    stops.append([row[0], row[2], stop_no, row[4]])
        read_file.close()
        return stops

    def get_direct_goo(self, postA, postB):

        self.postA = postA
        self.postB = postB
        url ='https://maps.googleapis.com/maps/api/directions/json?alternatives=true&transit_mode=bus&'
        print(self.postA)
        print(self.postB)

        req = requests.get(url + 'origin=' + self.postA +'&destination=' + self.postB
                         +'&sensor='+"false"+'&mode='+"transit"+'&key=' + google_key) # google_key imported from
        # passw.py in local

        return req.json()


    def needed_data(self, data):

        route_keys = [data["routes"][i].keys() for i, k in enumerate(data["routes"])]

        for i in range(len(route_keys)):
            for j in range(len(data["routes"][i]["legs"][0]["steps"])):

                if "transit_details" in data["routes"][i]["legs"][0]["steps"][j] and data["routes"][i]["legs"][0][
                    "steps"][j]["transit_details"]["line"]["vehicle"]["type"] == "BUS":

                    print("Vehicle: ", data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["line"]["vehicle"][
                        "type"])

                    print("dep stop: ", data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["departure_stop"])

                    print("headsign: ", data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["headsign"])

                    print("route name: ", data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["line"][
                        "short_name"])

                    print("num_stops: ", data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["num_stops"])

                    arr = int(data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["arrival_time"]["value"])
                    dep = int(data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["departure_time"]["value"])
                    tot = datetime.timedelta(seconds=(arr - dep))
                    print("total bus trip time: ", tot)

                    print("step number", j)
                    print("option number:", i)
                    print()

            print("-----------------------------------------------------")
            print()


    def connect_db(self):

        user = 'root'
        password = local_db_key
        host = '127.0.0.1'
        database = 'research'

        try:
            con = pymysql.connect(host=host, database=database, user=user, password=password)
        except Exception as e:
            sys.exit(e)

        cur = con.cursor()
        cur.execute("SELECT * FROM research.stops LIMIT 10")
        data = cur.fetchall()
        print(data)

