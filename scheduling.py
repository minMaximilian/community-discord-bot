from databaseClient import scheduler
from main import bot
import datetime
import time
from databaseClient import serversDB

def schedule(schedule_obj, game, guild_id):
    announce_in = schedule_obj['datetime'].timestamp() - time.time()
    scheduler.enter(announce_in, 1, makeAnnouncement(guild_id, game, schedule_obj['repeat']))

def re_schedule(guild_id, game):
    pass

def makeAnnouncement(guild_id, game, repeat):
    guild = bot.get_guild(guild_id)
    obj = serversDB.find_one({guild_id: {'$exists': True}})
    channel = guild.get_channel(obj[game]['channel'])
    channel.send(f'Game of {game} is starting now')
    if repeat:
        serversDB.update_one({guild_id: {'$exists': True}}, {guild_id: {game: {'schedule'}}})
        re_schedule(guild_id, game)