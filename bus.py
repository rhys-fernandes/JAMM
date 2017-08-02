from bs4 import BeautifulSoup
from requests import get

class BusTime:

    def __init__(self, items):
        self.page = get(
        "http://www.buscms.com/thamesdown/operatorpages/mobilesite/stop.aspx?stopid=ENTER_STOPID_HERE")
        self.soup = BeautifulSoup(self.page.content, "html.parser")
        self.no_of_times = items
        self.bus_times_dict = {}
        self.service = []
        self.bus_times = []
        self.get_bus_times()

    def get_bus_times(self):

        for i in self.soup.find_all("td", "colServiceName"):
            self.service.append(i.contents[0])

        for i in self.soup.find_all("td", "colDepartureTime"):
            self.bus_times.append(i.contents[0])

        for e in range(self.no_of_times):
            self.bus_times_dict[e] = self.service[e], self.bus_times[e]

        return self.bus_times_dict

