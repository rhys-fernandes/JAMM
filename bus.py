from bs4 import BeautifulSoup
from requests import get


class BusTime:

    def __init__(self, items):
        self.no_of_times = items
        self.bus_data = {}
        self.get_bus_times()

    def get_bus_times(self):
        self.bus_data.clear()
        page = get(
        "http://www.buscms.com/thamesdown/operatorpages/mobilesite/stop.aspx?stopid=47297")
        soup = BeautifulSoup(page.content, "html.parser")

        service = [x.contents[0] for x in soup.find_all("td", "colServiceName")]
        bus_times = [x.contents[0] for x in soup.find_all("td", "colDepartureTime")]

        self.bus_data = {i: (service[i], bus_times[i]) for i in range(self.no_of_times)}

        return self.bus_data
