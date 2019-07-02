import csv, re, requests, json
from passw import *
import MySQLdb


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

        direction_req = req.json()
        return json.dumps(direction_req)


    def connect_db(self):

        try:
            cnx = mysql.connector.connect(user='root', password=local_db_key,
                                          host='127.0.0.1',
                                          database='research')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()
