from model import *
from dao import Dao
from config.config import Config
from pymongo import MongoClient

config = Config()
mongo_client = MongoClient(host=config.get_mongo_url())

dao = Dao('newzealand', mongo_client=mongo_client)
plyer = dao.get_players_by_alias_from_all_regions('spud')