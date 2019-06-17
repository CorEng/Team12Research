import csv

def get():

    with open('stops.csv', encoding="utf8") as read_file:
        read_csv = csv.reader(read_file, delimiter=",")

        stops = []
        for i, row in enumerate(read_csv):
            stops.append([row[0], row[2], row[4]])

        read_file.close()

    return stops

print(get())