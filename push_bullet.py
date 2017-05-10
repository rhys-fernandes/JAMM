from pushbullet import Pushbullet
from configparser import ConfigParser

__config = ConfigParser()
__config.read("config.ini")

api_key = __config["ApiKeys"]["pushbullet"]
pb = Pushbullet(api_key)


def push_message(title, story):
    pb.push_link(title, story)
