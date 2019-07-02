import csv, re, requests, json


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
        api_key = 'AIzaSyBi-bH5_sngxNibrgygRZDhmAv2fK5hzus'
        url ='https://maps.googleapis.com/maps/api/directions/json?alternatives=true&'

        req = requests.get(url + 'origin=' + self.postA +'&destination=' + self.postB
                         +'&sensor='+"false"+'&mode='+"transit"+'&key=' + api_key)

        direction_req = req.json()
        return json.dumps(direction_req)


# print(Stops().get_all_stops())
