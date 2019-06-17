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