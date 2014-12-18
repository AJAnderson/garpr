import unittest
from dao import Dao, RegionNotFoundException, DuplicateAliasException, InvalidNameException
from bson.objectid import ObjectId
from model import *
from ming import mim
import trueskill
from datetime import datetime
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
import scraper.challonge
from scraper.challonge import ChallongeScraper

DATABASE_NAME = 'data'
PLAYERS_COLLECTION_NAME = 'players'
TOURNAMENTS_COLLECTION_NAME = 'tournaments'
RANKINGS_COLLECTION_NAME = 'rankings'
REGIONS_COLLECTION_NAME = 'regions'
USERS_COLLECTION_NAME = 'users'

TEST_TOURNEY = 983062

scraper = ChallongeScraper(TEST_TOURNEY)

mongo_client = MongoClient()
region = Region(7,'New Zealand')
##Dao.insert_region(region, mongo_client) 
p = Dao.get_all_regions(mongo_client)
mongo_client.close()
