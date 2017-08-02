import requests
import datetime as dt
from configparser import ConfigParser


class Weather(object):
    def __init__(self, location):
        __config = ConfigParser()
        __config.read("config.ini")

        self.api_id = __config["ApiKeys"]["owm"]
        self.location = location
        self.raw_weather_data = {}
        self.raw_forecast_data = {}
        self.request_data()

    def request_data(self):
        # noinspection PyPep8
        request_weather = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q=' +
            self.location + '&units=metric&appid=' + self.api_id)
        self.raw_weather_data = request_weather.json()

        # noinspection PyPep8
        request_forecast = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast?q=' +
            self.location + '&units=metric&appid=' + self.api_id)
        self.raw_forecast_data = request_forecast.json()

        # threading.Timer(5400, self.request_data).start() # independent use

    def get_weather(self, i):
        l_name = self.raw_weather_data["name"]
        l_temp = str(int(self.raw_weather_data["main"]["temp"])) + "°"
        l_weather = self.raw_weather_data["weather"][0]["main"]
        weather_desc = self.raw_weather_data["weather"][0]["description"]
        w_id = str(self.raw_weather_data["weather"][0]["id"])
        weather_data = {"name": l_name,
                        "temperature": l_temp,
                        "weather": l_weather,
                        "description": weather_desc,
                        "id": w_id}

        return weather_data[i]

    def forecast(self, i):
        f1_temp = str(
            int(self.raw_forecast_data["list"][6]["main"]["temp"])) + "°"
        f1_weather = self.raw_forecast_data["list"][6]["weather"][0]["main"]
        f1_id = str(self.raw_forecast_data["list"][6]["weather"][0]["id"])
        f1_data = {"temperature": f1_temp,
                   "weather": f1_weather,
                   "id": f1_id}
        f2_temp = str(
            int(self.raw_forecast_data["list"][14]["main"]["temp"])) + "°"
        f2_weather = self.raw_forecast_data["list"][14]["weather"][0]["main"]
        f2_id = str(self.raw_forecast_data["list"][14]["weather"][0]["id"])
        f2_data = {"temperature": f2_temp,
                   "weather": f2_weather,
                   "id": f2_id}

        f3_temp = str(
            int(self.raw_forecast_data["list"][22]["main"]["temp"])) + "°"
        f3_weather = self.raw_forecast_data["list"][22]["weather"][0]["main"]
        f3_id = str(self.raw_forecast_data["list"][22]["weather"][0]["id"])
        f3_data = {"temperature": f3_temp,
                   "weather": f3_weather,
                   "id": f3_id}

        day = {1: f1_data,
               2: f2_data,
               3: f3_data}

        return day[i]

    def sun_moon(self, i):
        r = str(int(self.raw_weather_data["sys"]["sunrise"]))
        s = str(int(self.raw_weather_data["sys"]["sunset"]))

        sunrise = dt.datetime.fromtimestamp(int(r)).strftime("%H:%M:%S")
        sunset = dt.datetime.fromtimestamp(int(s)).strftime("%H:%M:%S")

        s_m_data = {"rise": sunrise,
                    "set": sunset}

        return s_m_data[i]


# london = Weather("London")
# london.get_weather("description")
