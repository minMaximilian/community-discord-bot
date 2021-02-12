from pymongo import MongoClient

client = MongoClient(host='discord_bot_mongo', port=27017)

mongoDB = client.discord

serversDB = mongoDB.servers
usersDB = mongoDB.users