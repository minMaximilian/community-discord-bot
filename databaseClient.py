from pymongo import MongoClient

import sched, time

scheduler = sched.scheduler(time.time, time.sleep)

client = MongoClient(host='discord_bot_mongo', port=27017)

mongoDB = client.discord

serversDB = mongoDB.servers
usersDB = mongoDB.users