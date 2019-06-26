import csv
import re
import json


class Stops:

    def __init__(self):
        pass

    def get_all_stops(self):

        with open('stops.json', encoding="utf8") as read_file:
            read = json.load(read_file)

            stop = []
            for stop_no in read.keys():
                stop_name = read[stop_no]["stop_name"]
                if stop_no not in stop:
                    stop.append([stop_no, stop_name])
                elif stop_no in stop:
                    continue

            read_file.close()
        # print(stop)
        return stop

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
            start = [route for route in read[self.stopA]["routes"].keys()]
            end = [route for route in read[self.stopB]["routes"].keys()]

            final = {}
            for route in start:
                if (route in end):
                    for i, dest_noA in enumerate(read[self.stopA]["routes"][route]):
                        for j,dest_noB in enumerate(read[self.stopB]["routes"][route]):
                            if (read[self.stopA]["routes"][route][i][0] == read[self.stopB]["routes"][route][j][0]) \
                                    and (int(read[self.stopA]["routes"][route][i][1]) < int(read[self.stopB]["routes"][
                                route][j][1])):
                                if route not in final.keys():
                                    final[route] = [{"dest": read[self.stopA]["routes"][route][i][0], "seqA": read[
                                    self.stopA]["routes"][route][i][1], "seqB": read[self.stopB]["routes"][route][j][
                                        1]}]
                                elif route in final.keys():
                                    final[route].append([{"dest": read[self.stopA]["routes"][route][i][0], "seqA": read[
                                        self.stopA]["routes"][route][i][1], "seqB": read[self.stopB]["routes"][
                                        route][j][1]}])
                                else:
                                    continue

        # If bus route given by the user
        elif len(self.route) > 0:
            try:
                final = {}
                for i, k in enumerate(read[self.stopA]["routes"][route]):
                    for j, m in enumerate(read[self.stopB]["routes"][route]):
                        if (read[self.stopA]["routes"][route][i][0] == read[self.stopB]["routes"][route][j][0]) and \
                        (int(read[self.stopA]["routes"][route][i][1]) < int(read[self.stopB]["routes"][route][j][1])):
                            if route not in final.keys():
                                final[route] = [{"dest": read[self.stopA]["routes"][route][i][0], "seqA": read[
                                    self.stopA]["routes"][route][i][1], "seqB": read[self.stopB]["routes"][route][j][
                                    1]}]
                            elif route in final.keys():
                                final[route].append([{"dest": read[self.stopA]["routes"][route][i][0], "seqA": read[
                                    self.stopA]["routes"][route][i][1], "seqB": read[self.stopB]["routes"][
                                    route][j][1]}])
                            else:
                                continue
            except:
                print("The route given does not pass by these stops")


        final_routes = [route for route in final.keys()]

        stops = {}
        for route in final_routes:
            stops[route] = []
            # for stop in read.keys():
        #         try:
        #             dest_search = read[stop]["routes"][route]["dest"]
        #             dest_given = final[route]["dest"]
        #             seqA = int(final[route]["seqA"])
        #             seqB = int(final[route]["seqB"])
        #             seq_search = int(read[stop]["routes"][route]["seq"])
        #
        #             if (dest_search == dest_given) and (seq_search >= seqA) and (seq_search <= seqB) and (stop not in \
        #                     stops):
        #                 stops[route].append(stop)
        #         except:
        #             continue
        # read_file.close()
        #
        # return stops


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

                    if not stop[stop_no]["routes"]:
                        stop[stop_no]["routes"][route] = [(row[5], row[4])]

                    elif route not in stop[stop_no]["routes"].keys():
                        stop[stop_no]["routes"][route] = [(row[5], row[4])]

                    elif (route in stop[stop_no]["routes"].keys()) and ((row[5], row[4]) not in stop[stop_no][
                        "routes"][route]):
                        stop[stop_no]["routes"][route].append((row[5], row[4]))

                    else:
                        continue

        read_file.close()

        with open("stops.json", "w") as outfile:
            json.dump(stop, outfile)
        outfile.close()


a = Stops().a_to_b("2061","2065","155")


