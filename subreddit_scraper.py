import requests

class SubScraper:
    def __init__(self, subreddit, num):
        self.url = "https://www.reddit.com/r/{}.json".format(subreddit)
        self.no_of_stories = num
        self.main_stories = []
        self.links = []
        self.data = []

        self.fetch_data()


    def fetch_data(self):
        del self.main_stories[:]
        del self.links[:]
        del self.data[:]
        sauce = requests.get(self.url,
                             headers={'user-agent': 'Chrome'})

        raw_data = sauce.json()["data"]["children"]

        for data in raw_data[:self.no_of_stories]:
            self.main_stories.append(data["data"]["title"])
            self.links.append(data["data"]["url"])

        self.data.extend(zip(self.main_stories, self.links))


