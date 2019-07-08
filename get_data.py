import csv, re, requests, json, datetime
from passw import *
import pymysql


class Stops:

    def __init__(self):
        pass

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

                    print("arr stop: ", data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["arrival_stop"][
                        "name"])

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
        cur.execute("SELECT * FROM research.stops LIMIT 10") # Example
        data = cur.fetchall()
        print(data)


    def db_query(self, addre1, addre2):

        user='root'
        password='migmarache1982'
        host='127.0.0.1'
        database='research'

        try:
            con = pymysql.connect(host=host,database=database,user=user, password=password)
        except Exception as e:
            sys.exit(e)

        query = """SELECT stop_lat,stop_lon,stop_id,stop_name 
        FROM research.stops 
        WHERE stop_name LIKE %s or stop_name LIKE %s"""

        cur = con.cursor()
        cur.execute(query, (addre1, addre2),)
        data = cur.fetchall()
        cur.close()
        return data


    def db_query2(self, bus_no, stop_no, head_sign):

        user='root'
        password='migmarache1982'
        host='127.0.0.1'
        database='research'

        try:
            con = pymysql.connect(host=host,database=database,user=user, password=password)
        except Exception as e:
            sys.exit(e)

        query = """SELECT distinct research.stop_times.bus_number  
        FROM research.stop_times 
        WHERE research.stop_times.bus_number=%s and research.stop_times.bus_stop_number=%s 
        and research.stop_times.headsign=%s"""

        cur = con.cursor()
        cur.execute(query, (bus_no, stop_no, head_sign),)
        data = list(cur.fetchall())

        if len(data) > 0:
            data.pop()
            data.append(bus_no)
            data.append(head_sign)
        cur.close()
        return data


    def start_end(self, b, bus_no, head_sign):
        c = []
        for i in b:
            z = self.db_query2(bus_no, i[2], head_sign)
            if(len(z)!=0):
                z.append(i[0])
                z.append(i[1])
                z.append(i[2])
                z.append(i[3])
                c.append(z)
        return c


    def db_query3(self, head_sign, bus_no, stop_noA, stop_noB):

        user='root'
        password='migmarache1982'
        host='127.0.0.1'
        database='research'

        try:
            con = pymysql.connect(host=host,database=database,user=user, password=password)
        except Exception as e:
            sys.exit(e)

        query = """SELECT research.stop_times.bus_stop_number, research.stop_times.stop_sequence, research.trips.direction_id, research.stop_times.headsign 
        FROM research.stop_times, research.trips 
        WHERE stop_times.trip_id = trips.trip_id and stop_times.headsign = %s 
        and stop_times.bus_number = %s and (bus_stop_number = %s or bus_stop_number = %s)"""

        cur = con.cursor()
        cur.execute(query, (head_sign, bus_no, stop_noA, stop_noB),)
        cur.close()
        return cur.fetchall()


    def db_query4(self, bus_no, head_sign, seqA, seqB):

        user='root'
        password='migmarache1982'
        host='127.0.0.1'
        database='research'

        try:
            con = pymysql.connect(host=host,database=database,user=user, password=password)
        except Exception as e:
            sys.exit(e)

        query = """SELECT research.stops.stop_lat, research.stops.stop_lon, research.stop_times.bus_stop_number, 
        research.stop_times.stop_sequence, research.stop_times.headsign, research.stop_times.bus_number 
        FROM research.stop_times, research.stops
        WHERE bus_number = %s and headsign = %s and (stop_sequence between %s AND %s)
        LIMIT %s
        """

        limit = seqB - seqA + 1

        cur = con.cursor()
        cur.execute(query, (bus_no, head_sign, seqA, seqB, limit),)
        cur.close()
        return cur.fetchall()


    def final(self, a, addr1, addr2):

        route_keys = [a["routes"][i].keys() for i, k in enumerate(a["routes"])]

        for i in range(len(route_keys)):
            for j in range(len(a["routes"][i]["legs"][0]["steps"])):
                if "transit_details" in a["routes"][i]["legs"][0]["steps"][j] and a["routes"][i]["legs"][0]["steps"][j]["transit_details"]["line"]["vehicle"]["type"] == "BUS":

                    dep_stop = a["routes"][i]["legs"][0]["steps"][j]["transit_details"]["departure_stop"]["name"]
                    arr_stop = a["routes"][i]["legs"][0]["steps"][j]["transit_details"]["arrival_stop"]["name"]
                    bus_no = a["routes"][i]["legs"][0]["steps"][j]["transit_details"]["line"]["short_name"]
                    head_sign = a["routes"][i]["legs"][0]["steps"][j]["transit_details"]["headsign"]


                    b = self.db_query(dep_stop, arr_stop)
                    d = self.start_end(b, bus_no, head_sign)
                    print(d)
                    e = self.db_query3(d[0][1], d[0][0], d[0][4], d[1][4])
                    f = self.db_query4(d[0][0], e[0][3], e[0][1], e[1][1])
                    print(f)
                    print("step: ", j)
            print("option: ", i)
            print("*****************************************************************")