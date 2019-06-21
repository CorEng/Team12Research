import csv
import re
import json


class Stops:

    def __init__(self):
        pass

    def get_all_stops(self):

        with open('stops.json', encoding="utf8") as read_file:
            read = json.load(read_file)

            stops = []
            for stop in read.keys():
                lat = read[stop]["lat"]
                lon = read[stop]["lon"]
                stop_name = read[stop]["stop_name"]
                routes = [key for key in read[stop]["routes"].keys()]

                stops.append([lat, lon, stop_name, stop, routes])

            read_file.close()
        # print(stops)
        return stops

    def get_searched_stops(self, dict):

        if len(dict.keys()) == 0:
            print("No routes for the stops given")
        else:
            with open('stops.json', encoding="utf8") as read_file:
                read = json.load(read_file)

                stops = []
                for route in dict.keys():
                    for stop in dict[route]:
                        lat = read[stop]["lat"]
                        lon = read[stop]["lon"]
                        stop_name = read[stop]["stop_name"]
                        routes = [key for key in read[stop]["routes"].keys()]

                        stops.append([lat, lon, stop_name, stop, routes])

                read_file.close()

                return stops


    def a_to_b(self, stopA, stopB, route):
        self.stopA = stopA
        self.stopB = stopB
        self.route = route


        with open('stops.json', encoding="utf8") as read_file:
            read = json.load(read_file)

        # If no bus route given by the user
        if len(self.route) == 0:
            start = [route for i, route in enumerate(read[self.stopA]["routes"].keys())]
            end = [route for i, route in enumerate(read[self.stopB]["routes"].keys())]

            final = {}
            for i, route in enumerate(start):
                if (route in end) and (read[self.stopA]["routes"][route]["dest"] == read[self.stopB]["routes"][route][
                    "dest"]):
                    final[route] = {"dest": read[self.stopA]["routes"][route]["dest"], "seqA":read[self.stopA]["routes"][
                        route]["seq"], "seqB": read[self.stopB]["routes"][route]["seq"]}
                else:
                    continue

        # If bus route given by the user
        elif len(self.route) > 0:
            try:
                final = {}
                final[self.route] = {"dest": read[self.stopA]["routes"][route]["dest"], "seqA":read[self.stopA]["routes"][
                    route]["seq"], "seqB": read[self.stopB]["routes"][route]["seq"]}

            except:
                pass

        final_routes = [route for i, route in enumerate(final.keys())]

        stops = {}
        for i, route in enumerate(final_routes):
            stops[route] = []
            for k, key in enumerate(read.keys()):
                try:
                    dest_search = read[key]["routes"][route]["dest"]
                    dest_given = final[route]["dest"]
                    seqA = int(final[route]["seqA"])
                    seqB = int(final[route]["seqB"])
                    seq_search = int(read[key]["routes"][route]["seq"])

                    if (dest_search == dest_given) and (seq_search >= seqA) and (seq_search <= seqB) and (key not in \
                            stops):
                        stops[route].append(key)
                except:
                    continue
        read_file.close()

        return stops


    def create_json(self):

        regex = re.compile("(\-[\w]+\-)")
        no_ceros = re.compile("[1-9][0-9]*")

        # Main dictionary
        stop = {}
        with open('stops.csv', encoding="utf8") as read_file:
            read_csv = csv.reader(read_file, delimiter=",")

            for i, row in enumerate(read_csv):
                if i == 0:
                    continue
                else:
                    stop_no = no_ceros.search(row[3][-6:]).group()
                    stop[stop_no] = {"lat": float(row[0]), "lon": float(row[2]), "stop_name": row[4],
                                    "routes": {}}
        read_file.close()

        with open('stop_times.csv', encoding="utf8") as read_file:
            read_csv = csv.reader(read_file, delimiter=",")

            for i, row in enumerate(read_csv):
                if i == 0:
                    continue
                else:
                    route = regex.search(row[0]).group()
                    route = route[1:-1]
                    stop_no = no_ceros.search(row[3][-6:]).group()
                    if stop[stop_no]["routes"].get(route) == route:
                        continue
                    elif stop[stop_no]["routes"].get(route) == None:
                        stop[stop_no]["routes"][route] = {"dest":row[5], "seq":row[4]}


        read_file.close()

        with open("stops.json", "w") as outfile:
            json.dump(stop, outfile)
        outfile.close()


# a = Stops()
# a.get_stops()
# print(a.a_to_b("2062", "4727", "84X"))
# b = a.a_to_b("2062", "4727", "84X")
# a.get_searched_stops(b)
# a.a_to_b("7556", "7430")




