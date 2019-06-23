import requests
from peewee import *


class Weather(Model):
    time = IntegerField(primary_key=True)
    summary = CharField(max_length=255, null=True)
    icon = CharField(max_length=255, null=True)
    precipIntensity = FloatField(null=True)
    precipType = CharField(max_length=255, null=True)
    apprentTemperature = FloatField(null=True)
    dewPoint = FloatField(null=True)
    humidity = FloatField(null=True)
    pressure = FloatField(null=True)
    windSpeed = FloatField(null=True)
    windGuest = FloatField(null=True)
    windBearing = IntegerField(null=True)
    cloudCover = IntegerField(null=True)
    uvIndex = IntegerField(null=True)
    visibility = FloatField(null=True)

    class Meta:
        database = MySQLDatabase('mydb', user='root', password='abc',
                                 host='127.0.0.1', port=3306)


def init_db():
    db = MySQLDatabase('mydb', user='root', password='abc',
                       host='127.0.0.1', port=3306)

    db.connect()
    db.create_tables([Weather])


if __name__ == '__main__':
    init_db()

    for d in range(1514764800, 1546300799, 86400):
        url = f"https://api.darksky.net/forecast/ae6a76d9d2a422cd7efb48155608e3e5/53.3498,6.2603,{d}?exclude=currently,minutely,daily'"

        result = requests.get(url)

        if result.status_code == 200:
            data = result.json()['hourly']['data']

            for record in data:
                weather = Weather.create(time=record['time'],
                                         summary=record.get('summary', None),
                                         icon=record.get('icon', None),
                                         precipIntensity=record.get('precipIntensity', None),
                                         precipProbability=record.get('precipProbability', None),
                                         precipType=record.get('precipType', None),
                                         temperature=record.get('temperature', None),
                                         apparentTemperature=record.get('apparentTemperature', None),
                                         dewPoint=record.get('dewPoint', None),
                                         humidity=record.get('humidity', None),
                                         pressure=record.get('pressure', None),
                                         windSpeed=record.get('windSpeed', None),
                                         windGust=record.get('windGust', None),
                                         windBearing=record.get('windBearing', None),
                                         cloudCover=record.get('cloudCover', None),
                                         uvIndex=record.get('uvIndex', None),
                                         visibility=record.get('visibility', None)
                                         )
                weather.save()
