import discord

from discord.ext import commands
from databaseClient import serversDB

import json

class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Used to test if the bot is functioning, responds with a pong')
    async def ping(self, ctx):
        await ctx.reply('pong', mention_author=False)

    @commands.command(name='registry', help='Shows a tabulation of all users registered')
    @commands.is_owner()
    @commands.guild_only()
    async def registry(self, ctx, game:str):
        file_name = str(ctx.guild.id) + ".json"
        with open(file_name, "r") as f:
            data = json.load(f)
        if str(game.lower()) in data:
            with open(file_name, "w") as f:
                await ctx.reply(f'Succesfully set the {ctx.message.channel.mention} channel as the registry for {game}', mention_author=False, delete_after=3.0)
                embed = await ctx.send(embed=await self.generateEmbed(data, game))
                data[str(game.lower())]['registry']['channel']=ctx.message.channel.id
                data[str(game.lower())]['registry']['embed']=embed.id
                json.dump(data, f, indent=4)
        else:
            await ctx.reply(f'Couldn\'t find the game within the possible candidates')

    @commands.command(name='register', help='Allows registration for a the ingame tag')
    @commands.guild_only()
    async def register(self, ctx, tag:str, game:str):             
                # if 'embed' in data[str(game.lower())]['registry']:
                #     channel = self.bot.get_channel(int(data[str(game.lower())]['registry']['channel']))
                #     embed = await channel.fetch_message(int(data[str(game.lower())]['registry']['embed']))
                #     await embed.edit(embed=await self.generateEmbed(data, game))
        if serversDB.find({str(ctx.guild.id) + "." + game.lower(): {'$exists': True}}).count() > 0:
            insertion = serversDB.find_one({str(ctx.guild.id): {'$exists': True}})
            payload = {
                    str(ctx.author.id): tag
            }   
            insertion[str(ctx.guild.id)][game.lower()]['registry']['players'] = payload
            serversDB.save(insertion)
            await ctx.reply(f'Succesfully added {tag} to the player {ctx.message.author.mention} to the {game.capitalize()} registry', mention_author=False)
        else:
            await ctx.reply(f'{game.capitalize()} is not a possible canddiate for registries, try correcting the game name')
            
    @commands.command(name='addGame', help='Adds the game as a possible candidate for scheduling and registries')
    @commands.is_owner()
    @commands.guild_only()
    async def addGame(self, ctx, game:str):
        if serversDB.find({str(ctx.guild.id) + "." + game.lower(): {'$exists': True}}).count() > 0:
            await ctx.reply(f'{game.capitalize()} already exists as a possible candidate')
        else:
            insertion = serversDB.find_one({str(ctx.guild.id): {'$exists': True}})
            payload = {
                    'registry': {'players': {}},
                    'schedule': {}
            }   
            insertion[str(ctx.guild.id)][game.lower()] = payload
            serversDB.save(insertion)
            await ctx.reply(f'Succesfully added {game.capitalize()} as a possible candidate for scheduling and registries')
        
    
    @commands.command(name='removeGame', help='Adds a game to be used within scheduler commands')
    @commands.is_owner()
    @commands.guild_only()
    async def removeGame(self, ctx, game: str):
        if serversDB.find({str(ctx.guild.id) + "." + game.lower(): {'$exists': True}}).count() > 0:
                serversDB.update({str(ctx.guild.id): {'$exists': True}}, {'$unset': {str(ctx.guild.id) + "." + game.lower(): {}}})
                await ctx.reply(f'{game.capitalize()} succesfully removed')
        else:
            await ctx.reply(f'{game.capitalize()} doesn\'t exist')

    @commands.command(name='addSchedule', help='Schedules the game')
    @commands.guild_only()
    async def addSchedule(self, ctx, schedule, game: str):
        await ctx.reply(f'Succesfully scheduled a game @{schedule} for {game.capitalize()}')

    @commands.command(name='removeSchedule', help='Removes scheduled item')
    @commands.guild_only()
    async def removeSchedule(self, ctx, schedule, game: str):
        await ctx.reply(f'Succesfully unscheduled a game @{schedule} for {game.capitalize()}')

    async def generateEmbed(self, data, game):
        iterable = data[game.lower()]['registry']['players'].items()
        descriptor = ''
        for key, val in iterable:
            descriptor += f'<@{key}>: {val}\n'
        return discord.Embed(title=f"Concurrently {len(iterable)} registered for {game.capitalize()}", description=descriptor)
