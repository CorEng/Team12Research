import csv

def get_stops():

    with open('stops.csv', encoding="utf8") as read_file:
        read_csv = csv.reader(read_file, delimiter=",")

        stops = []
        count = 0
        for i, row in enumerate(read_csv):
            if i == 0:
                continue
            else:
                if not float(row[0]) or not float(row[2]):
                    print(count)
                else:
                    stops.append([float(row[0]), float(row[2]), row[4]])
            count += 1

        read_file.close()

    return stops


def start():

    # Main dictionary
    stop_name = {}
    with open('stops.csv', encoding="utf8") as read_file:
        read_csv = csv.reader(read_file, delimiter=",")

        for i, row in enumerate(read_csv):
            if i == 0:
                continue
            else:
                stop_name[row[3]] = {"lat": float(row[0]), "lon": float(row[2]), "stop_name": row[4], "tripId": [],
                                "routeId": [], "routes": []}

    read_file.close()


    # Join Route Id with route short name
    route_no = {}
    with open('routes.csv', encoding="utf8") as read_file:
        read_csv = csv.reader(read_file, delimiter=",")

        for i, row in enumerate(read_csv):
            if i == 0:
                continue
            else:
                route_no[row[7]] = row[1]

    read_file.close()


    stop_trip = {}
    with open('stop_times.csv', encoding="utf8") as read_file:
        read_csv = csv.reader(read_file, delimiter=",")

        for i, row in enumerate(read_csv):
            if i == 0:
                continue
            else:
                try:
                    stop_trip[row[0]].append(row[3])
                except:
                    stop_trip[row[0]] = [row[3]]



    read_file.close()
    print(stop_trip["13687.2.60-150-b12-1.83.O"])

# start()