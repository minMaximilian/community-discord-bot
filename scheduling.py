from databaseClient import scheduler
from main import bot
import datetime
import time
from databaseClient import serversDB

def schedule(schedule_obj, game, guild_id):
    announce_in = schedule_obj['datetime'].timestamp() - time.time()
    scheduler.enter(announce_in, 1, makeAnnouncement(guild_id, game, schedule_obj['repeat'], schedule_obj['timestamp']))

def makeAnnouncement(guild_id, game, repeat, timestamp):
    guild = bot.get_guild(guild_id)
    obj = serversDB.find_one({guild_id: {'$exists': True}})
    channel = guild.get_channel(obj[game]['channel'])
    channel.send(f'Game of {game} is starting now')
    if repeat:
        newSchedule = datetime.datetime.strptime(datetime.datetime.now(), '%Y-%m-%d %H:%M') + datetime.timedelta(days=7)
        payload = {'datetime': newSchedule, 'timestamp': timestamp, 'repeat': repeat}        
        serversDB.update_one({f'{guild_id}.{game.lower()}.schedule.timestamp': timestamp}, {'$set': {f'{guild_id}.{game.lower()}.schedule.$.datetime': newSchedule}})
        schedule(payload, game, guild_id)