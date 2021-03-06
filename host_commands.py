import discord
import datetime
import time
import calendar
import scheduling

from discord.ext import commands
from databaseClient import serversDB

class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='registry', help='Shows a tabulation of all users registered')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def registry(self, ctx, game:str):
        if serversDB.find({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}).count() > 0:
                await ctx.reply(f'Succesfully set the {ctx.message.channel.mention} channel as the registry for {game}', mention_author=False, delete_after=3.0)
                embed = await ctx.send(embed=await self.generateEmbed(ctx, game))
                serversDB.update({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}, {'$set': {f'{ctx.guild.id}.{game.lower()}.registry.embed': embed.id, f'{ctx.guild.id}.{game.lower()}.registry.channel': ctx.message.channel.id}},upsert=True)
        else:
            await ctx.reply(f'Couldn\'t find the game within the possible candidates')

    @commands.command(name='register', help='Allows registration for a the ingame tag')
    @commands.guild_only()
    async def register(self, ctx, tag:str, game:str):
        queryResult = serversDB.find_one({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}) 
        if queryResult:
            serversDB.update({str(ctx.guild.id): {'$exists': True}}, {'$set': {f'{ctx.guild.id}.{game.lower()}.registry.players.{ctx.author.id}': tag}}, upsert=True)
            await ctx.reply(f'Succesfully added {tag} to the player {ctx.message.author.mention} to the {game.capitalize()} registry', mention_author=False)
            if queryResult[str(ctx.guild.id)][game.lower()]['registry']['embed']:
                channel = self.bot.get_channel(int(queryResult[str(ctx.guild.id)][game.lower()]['registry']['channel']))
                embed = await channel.fetch_message(int(queryResult[str(ctx.guild.id)][game.lower()]['registry']['embed']))
                await embed.edit(embed=await self.generateEmbed(ctx, game))
            if queryResult[str(ctx.guild.id)][game.lower()]['role']:
                user = ctx.message.author
                role = ctx.guild.get_role(queryResult[str(ctx.guild.id)][game.lower()]['role'])
                await   user.add_roles(role)
        else:
            await ctx.reply(f'{game.capitalize()} is not a possible candidate for registries, try correcting the game name')

    @commands.command(name='deregister', help='Allows deregistration from a game')
    @commands.guild_only()
    async def deregister(self, ctx, game:str):
        await self.removeFromRegistration(ctx, ctx.author, game)

    @commands.command(name='removeRegistration', help='Allows deregistration from a game')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def removeRegistration(self, ctx, user: discord.Member, game:str):
        await self.removeFromRegistration(ctx, user, game)

    async def removeFromRegistration(self, ctx, user, game):
        queryResult = serversDB.find_one({f'{ctx.guild.id}.{game.lower()}.registry.players.{user.id}': {'$exists': True}}) 
        if queryResult:
            serversDB.update_one({str(ctx.guild.id): {'$exists': True}}, {'$unset': {f'{ctx.guild.id}.{game.lower()}.registry.players.{user.id}': ''}})
            await ctx.reply(f'Succesfully deregistered {user.mention} from the {game.capitalize()} registry', mention_author=False)
            if queryResult[str(ctx.guild.id)][game.lower()]['registry']['embed']:
                channel = self.bot.get_channel(int(queryResult[str(ctx.guild.id)][game.lower()]['registry']['channel']))
                embed = await channel.fetch_message(int(queryResult[str(ctx.guild.id)][game.lower()]['registry']['embed']))
                await embed.edit(embed=await self.generateEmbed(ctx, game))
            if queryResult[str(ctx.guild.id)][game.lower()]['role']:
                role = ctx.guild.get_role(queryResult[str(ctx.guild.id)][game.lower()]['role'])
                if role in user.roles:
                    await user.remove_roles(role)
        else:
            await ctx.reply(f'{game.capitalize()} is not a possible candidate for deregistration, or the person you want to deregister isn\'t registered')
            
    @commands.command(name='wipeGame', help='Adds the game as a possible candidate for scheduling and registries')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def wipeGame(self, ctx, game:str):
        queryResult = serversDB.find_one({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}) 
        if queryResult:
            registry = queryResult[str(ctx.guild.id)][game.lower()]['registry']['players']
            if queryResult[str(ctx.guild.id)][game.lower()]['role']:
                role = ctx.guild.get_role(queryResult[str(ctx.guild.id)][game.lower()]['role'])
                for key, _ in registry.items():
                    user = ctx.message.guild.get_member(int(key))
                    if user:
                        if role in user.roles:
                            await user.remove_roles(role)

            if serversDB.find({f'{ctx.guild.id}.{game.lower()}.registry.embed': {'$exists': True}}).count() > 0:
                channel = self.bot.get_channel(int(queryResult[str(ctx.guild.id)][game.lower()]['registry']['channel']))
                embed = await channel.fetch_message(int(queryResult[str(ctx.guild.id)][game.lower()]['registry']['embed']))
                await embed.edit(embed=await self.generateEmbed(ctx, game))
            
            serversDB.update({str(ctx.guild.id): {'$exists': True}}, {'$set': {f'{ctx.guild.id}.{game.lower()}.registry.players': {}}}, upsert=True)
            await ctx.reply(f'Succesfully wiped the registry of {game.lower()}')

        else:
            await ctx.reply(f'{game.capitalize()} is not a possible candidate for registries, try correcting the game name')

        

    @commands.command(name='addGame', help='Adds the game as a possible candidate for scheduling and registries')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def addGame(self, ctx, game:str, role: discord.Role = None):
        if serversDB.find({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}).count() > 0:
            await ctx.reply(f'{game.capitalize()} already exists as a possible candidate')
        else:
            payload = {
                    'registry': {'players': {}},
                    'schedule': [],
            }
            if role:
                payload['role'] = role.id

            serversDB.update({str(ctx.guild.id): {'$exists': True}}, {'$set': {f'{ctx.guild.id}.{game.lower()}': payload}}, upsert=True)
            await ctx.reply(f'Succesfully added {game.capitalize()} as a possible candidate for scheduling and registries')
        
    
    @commands.command(name='removeGame', help='Adds a game to be used within scheduler commands')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def removeGame(self, ctx, game: str):
        if serversDB.find({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}).count() > 0:
                serversDB.update({str(ctx.guild.id): {'$exists': True}}, {'$unset': {f'{ctx.guild.id}.{game.lower()}': {}}})
                await ctx.reply(f'{game.capitalize()} succesfully removed')
        else:
            await ctx.reply(f'{game.capitalize()} doesn\'t exist')

    @commands.command(name='addSchedule', help='Schedules the games the game, command format "?addSchedule "Year-Month-Day Hour-Minute" GameName Repeat(True|False)", the bot figures out the day and repeats the schedule, unless repeat is False, on by default')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def addSchedule(self, ctx, schedule, game: str, repeat: bool = True):
        response = serversDB.find_one({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}})
        if response:
            scheduledObj = datetime.datetime.strptime(schedule, '%Y-%m-%d %H:%M')
            if scheduledObj > datetime.datetime.now():
                payload = {'datetime': scheduledObj, 'timestamp': int(time.time()), 'repeat': repeat}        
                serversDB.update_one({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}, {'$push': {f'{ctx.guild.id}.{game.lower()}.schedule': payload}}, upsert=True)
                await scheduling.schedule(payload, game, ctx.guild.id, self.bot)
                await ctx.reply(f'Succesfully scheduled a game for {game.capitalize()} at {schedule}')
            else:
                await ctx.reply(f'The programmer is a dummy and can\'t and doesn\'t want to program user proof commands so please make sure the date scheduled is actually in the future')
        else:
            await ctx.reply(f'{game.capitalize()} doesn\'t exist as a possible candidate for scheduling and registries')

    @commands.command(name='removeSchedule', help='Removes scheduled item')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def removeSchedule(self, ctx, timestamp:int, game: str):
        response = serversDB.find_one({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}})
        if response:
            serversDB.update_one({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}}, {'$pull': {f'{ctx.guild.id}.{game.lower()}.schedule': {'timestamp': timestamp}}})
            await ctx.reply(f'Succesfully unscheduled a game @{timestamp} for {game.capitalize()}')
        else:
            await ctx.reply(f'{game.capitalize()} is not a possible canddiate for registries, try correcting the game name')

    @commands.command(name='showSchedule', help='Shows scheduled items')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def showSchedule(self, ctx, game: str):
        data = serversDB.find_one({f'{ctx.guild.id}.{game.lower()}': {'$exists': True}})
        if data:
            await ctx.send(embed= await self.generateSchedules(data, ctx.guild.id, game.lower()))
        else:
            await ctx.reply(f'{game.capitalize()} is not a possible canddiate for registries, try correcting the game name')

    async def generateSchedules(self, data, guildID, game):
        descriptor = ''
        for i in data[str(guildID)][game]['schedule']:
            ID = i['timestamp']
            date = i['datetime']
            calendar_day = calendar.day_name[date.weekday()]
            if i['repeat']:
                descriptor += f'**ID: {ID}** \n Every *{calendar_day}* at {date.time()}\n\n'
            else:
                descriptor += f'**ID: {ID}** \n Scheduled for {date}\n\n'
        return discord.Embed(title=f'Scheduled games for {game.capitalize()}', description=descriptor)

    async def generateEmbed(self, ctx, game):
        iterable = serversDB.find_one({f'{ctx.guild.id}': {'$exists': True}}, {f'{ctx.guild.id}.{game.lower()}.registry.players': 1})
        iterable = iterable[str(ctx.guild.id)][game.lower()]['registry']['players']
        descriptor = ''
        for key, val in iterable.items():
            descriptor += f'<@{key}>: \n *{val}*\n\n'
        return discord.Embed(title=f'Concurrently {len(iterable.items())} registered for {game.capitalize()}', description=descriptor)

    # Need to add skanderbeg integration down here