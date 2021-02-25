from databaseClient import scheduler
from main import bot
import datetime
import time

def schedule(schedule_obj, game, guild_id):
    announce_in = schedule_obj['datetime'].timestamp() - time.time()
    scheduler.enter(announce_in, 1, makeAnnouncement(guild_id, game))

def re_schedule():
    pass

def makeAnnouncement(guild_id, game):
    guild = bot.get_guild(guild_id)
    guild.get_channel()
    