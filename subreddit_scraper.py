import requests


class SubScraper:
    def __init__(self, subreddit, num):
        self.url = "https://www.reddit.com/r/{}.json".format(subreddit)
        self.no_of_stories = num
        self.main_stories = []
        self.links = []

        self.fetch_data()

        self.data = list(zip(self.main_stories, self.links))

    def fetch_data(self):
        sauce = requests.get(self.url,
                             headers={'user-agent': 'Chrome'})

        raw_data = sauce.json()["data"]["children"]

        for data in raw_data[:self.no_of_stories]:
            self.main_stories.append(data["data"]["title"])
            self.links.append(data["data"]["url"])
