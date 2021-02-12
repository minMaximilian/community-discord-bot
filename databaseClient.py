from pymongo import MongoClient

client = MongoClient(host='discord_bot_mongo', port=27017)

mongoDB = client.discord

gamesDB = mongoDB.games
usersDB = mongoDB.users