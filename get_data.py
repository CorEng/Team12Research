import csv
import re


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


# print(Stops().get_all_stops())
