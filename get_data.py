import requests, datetime, pymysql, sys, difflib
from operator import itemgetter
from datetime import date, time, timedelta
from tweepy import OAuthHandler, API, Cursor


class Stops:

    def __init__(self):
        self.goahead = ["17", "17a", "18", "33a", "33b", "45a", "45b", "59", "63", "63a", "75", "75a", "76", "76a",
                        "102", "104", "111", "114", "161", "175", "184", "185", "220", "236", "238", "239", "270"]
        self.post_a = None
        self.post_b = None
        self.secs = None
        self.date = None
        self.time = None
        self.type = None
        self.list = None

        self.final_amenities = []
        
    def get_direct_goo(self, post_a, post_b, secs, dep_arr_time):

        self.post_a = post_a
        self.post_b = post_b
        self.secs = secs
        if dep_arr_time == "dep":
            dep_arr_time = '&departure_time='
        elif dep_arr_time == "arr":
            dep_arr_time = '&arrival_time='

        url = 'https://maps.googleapis.com/maps/api/directions/json?alternatives=true&transit_mode=bus&'

        req = requests.get(f"{url}origin={self.post_a}&destination={self.post_b}{dep_arr_time}{secs}"
                           f"&sensor=false&mode=transit&key=AIzaSyAf6-Rcx8RSnbzJELLh1dmpoBAOHh70Ax4")

        return req.json()

    @staticmethod
    def lat_lon(bus_no, head_sign, goo_lat, goo_lon):

        user = 'root'
        password = "abc"
        host = '127.0.0.1'
        database = 'research'

        try:
            con = pymysql.connect(host=host, database=database, user=user, password=password)
        except Exception as e:
            sys.exit(e)

        lat = round(float(goo_lat), 4)
        lon = round(float(goo_lon), 4)

        query = """SELECT distinct stop_lat, stop_lon, stop_id, stop_name 
                FROM research.stops, research.stop_times
                WHERE research.stop_times.bus_stop_number = research.stops.stop_id 
                    and research.stop_times.bus_number = %s
                    and research.stop_times.headsign = %s
                    and ((stop_lat BETWEEN %s and %s) and (stop_lon BETWEEN %s and %s));"""

        cur = con.cursor()
        cur.execute(query, (bus_no, head_sign, lat - 0.001, lat + 0.001, lon - 0.001, lon + 0.001), )
        data = cur.fetchall()
        if len(data) < 1:
            cur.execute(query, (bus_no, head_sign, lat - 0.003, lat + 0.003, lon - 0.003, lon + 0.003), )
            data = cur.fetchall()
        cur.close()

        return tuple(data)

    @staticmethod
    def filter_name(stops_list, google_name):

        final = ()

        ratio = 0
        for stop in stops_list:
            stop_ratio = difflib.SequenceMatcher(None, stop[3], google_name).ratio()
            if stop_ratio > ratio:
                ratio = stop_ratio
                final = stop

        return final

    @staticmethod
    def db_query3(head_sign, bus_no, stop_no_a, stop_no_b, diff):

        user = 'root'
        password = 'abc'
        host = '127.0.0.1'
        database = 'research'

        try:
            con = pymysql.connect(host=host, database=database, user=user, password=password)
        except Exception as e:
            sys.exit(e)

        query = """SELECT research.stop_times.bus_stop_number, research.stop_times.stop_sequence, 
        research.stop_times.headsign, research.trips.trip_id
            FROM research.stop_times, research.trips
            WHERE research.stop_times.trip_id = research.trips.trip_id
                and stop_times.headsign = %s 
                and stop_times.bus_number = %s 
                and (bus_stop_number = %s or bus_stop_number = %s)"""

        cur = con.cursor()
        cur.execute(query, (head_sign, bus_no, stop_no_a, stop_no_b), )
        cur.close()
        data = cur.fetchall()

        final = []

        for i, value in enumerate(data):
            if i == 0:
                final.append(value)
            else:
                if value[1] - final[0][1] == diff:
                    final.append(value)

        return tuple(final)

    @staticmethod
    def db_query4(bus_no, head_sign, seq_a, seq_b, trip_id):

        user = 'root'
        password = "abc"
        host = '127.0.0.1'
        database = 'research'

        try:
            con = pymysql.connect(host=host, database=database, user=user, password=password)
        except Exception as e:
            sys.exit(e)

        query = """SELECT research.stops.stop_lat, research.stops.stop_lon, research.stop_times.bus_stop_number, 
                research.stop_times.stop_sequence, research.stop_times.headsign, research.stop_times.bus_number,
                research.stops.stop_name 
                FROM research.stop_times, research.stops, research.trips
                WHERE research.stop_times.bus_stop_number = research.stops.stop_id
                    and research.trips.trip_id = research.stop_times.trip_id
                    and research.stop_times.bus_number = %s 
                    and research.stop_times.headsign = %s 
                    and (research.stop_times.stop_sequence between %s AND %s)
                    and research.stop_times.trip_id = %s
                """

        cur = con.cursor()
        cur.execute(query, (bus_no, head_sign, seq_a, seq_b, trip_id), )
        cur.close()
        # sorted(student_tuples, key=itemgetter(2))
        ordered = sorted(list(cur.fetchall()), key=itemgetter(3))
        return ordered

    def fin(self, goo_data):

        route_keys = [goo_data["routes"][i].keys() for i, k in enumerate(goo_data["routes"])]
        all_opts = []
        for i in range(len(route_keys)):
            option = []
            for j in range(len(goo_data["routes"][i]["legs"][0]["steps"])):

                if "transit_details" in goo_data["routes"][i]["legs"][0]["steps"][j] and \
                        goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["line"]["vehicle"][
                            "type"] == "BUS":

                    dep_stop = goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["departure_stop"][
                        "name"].strip()
                    arr_stop = goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["arrival_stop"][
                        "name"].strip()
                    bus_no = goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["line"][
                        "short_name"].strip()
                    head_sign = goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["headsign"].strip()
                    num_stops = goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["num_stops"]

                    lat_a = \
                        goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["departure_stop"]["location"][
                            "lat"]
                    lon_a = \
                        goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["departure_stop"]["location"][
                            "lng"]

                    lat_b = goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["arrival_stop"]["location"][
                        "lat"]
                    lon_b = goo_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["arrival_stop"]["location"][
                        "lng"]

                    print("Option:", i, "leg", j)
                    print("Details from google:")
                    print("dep_stop:", dep_stop)
                    print("arr_stop:", arr_stop)
                    if bus_no in self.goahead:
                        print("bus_no:", bus_no, "**FROM GOAHEAD**")
                    else:
                        print("bus_no:", bus_no)
                    print("num_stops: ", num_stops)
                    print("head_sign:", head_sign)
                    print("lat/lon A:", lat_a, lon_a)
                    print("lat/lon B:", lat_b, lon_b)
                    print()

                    print("1st Query - lat_lon ----------------------")
                    print("stopA")
                    one_a = self.lat_lon(bus_no, head_sign, lat_a, lon_a)
                    print(one_a)
                    print()
                    print("stopB")
                    one_b = self.lat_lon(bus_no, head_sign, lat_b, lon_b)
                    print(one_b)
                    print()

                    if len(one_a) > 0 and len(one_b) > 0:
                        print("filter 1st query by name -----------------------")
                        print("stopA")
                        two_a = self.filter_name(one_a, dep_stop)
                        print(two_a)
                        print()
                        print("stopB")
                        two_b = self.filter_name(one_b, arr_stop)
                        print(two_b)
                        print()

                        if two_a and two_b:
                            print("Query 3 - get seq and direction id -------------")
                            # Stop A and stop B here have to be the ones from our filters not from google
                            three = self.db_query3(head_sign, bus_no, two_a[2], two_b[2], num_stops)
                            print(three)
                            print()

                            if len(three) == 2:
                                print("Query 4 - obtain intermediate stops ------------")
                                # Pass only the 1st two stops given by previous query
                                four = self.db_query4(bus_no, head_sign, three[0][1], three[1][1], three[0][3])
                                option.append(four)
                                print(four)
                                print()

                            else:
                                print("ERROR: query 3 does not have 2 items - it has:", len(three), "items")
                                pass
                        else:
                            print("ERROR: length of twoA:", len(two_a), "length of twoB:", len(two_b))
                            pass
                    else:
                        print("ERROR: length of oneA is", len(one_a), "length of oneB:", len(one_b))
                        pass

                    print()
            all_opts.append(option)
            print("-------------------------------------------------------------------------------------------")
        return all_opts

    def get_seconds(self, date, time):
        self.date = date
        self.time = time + ":00"

        current_time_date = datetime.datetime.now()

        if len(self.date) < 1:
            self.date = current_time_date.strftime("%Y-%m-%d")
        if len(self.time) < 4:
            self.time = current_time_date.strftime("%H:%M:%S")

        date_time = self.date + " " + self.time
        time_obj = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

        seconds = round(time_obj.timestamp())

        return str(seconds)

    def get_amenities(self, type, list):

        self.type = type
        self.list = list

        self.final_amenities = []

        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

        for option in self.list:
            op_list = []
            for leg in option:
                for stop in leg:
                    location = str(stop[0]) + "," + str(stop[1])
                    req = requests.get(url + "location=" + location + "&radius=50&type=" + self.type
                                       + "&fields=formatted_address,geometry,name&key=" + "AIzaSyAf6-Rcx8RSnbzJELLh1dmpoBAOHh70Ax4")

                    if req.json()["status"] == "OK":
                        op_list.append(req.json()["results"])

            self.final_amenities.append(op_list)

        return self.final_amenities

    @staticmethod
    def notification_check(goog_data):

        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        auth_api = API(auth)

        end_date = datetime.datetime.utcnow() - timedelta(days=1)
        tweet_list = []

        for i in range(len(goog_data["routes"])):
            option = []
            for j in range(len(goog_data["routes"][i]["legs"][0]["steps"])):

                if "transit_details" in goog_data["routes"][i]["legs"][0]["steps"][j] and \
                        goog_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["line"]["vehicle"][
                            "type"] == "BUS":

                    route = goog_data["routes"][i]["legs"][0]["steps"][j]["transit_details"]["line"][
                        "short_name"].strip()

                    for status in Cursor(auth_api.user_timeline, id="@dublinbusnews").items():
                        if "#DBSvcUpdate" in status.text:
                            if ("#DB" + route) in status.text or (
                                    "Diversion" in status.text) and status.text not in option:
                                option.append(status.text)
                        if status.created_at < end_date:
                            break
            tweet_list.append(option)

        return tweet_list
