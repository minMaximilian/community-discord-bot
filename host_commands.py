import discord

from discord.ext import commands
import json

class Host(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Used to test if the bot is functioning, responds with a pong')
    async def ping(self, ctx):
        await ctx.reply('pong', mention_author=False)

    @commands.command(name='registry', help='Shows a tabulation of all users registered')
    async def registry(self, ctx, game:str):
        await ctx.reply('Registry', mention_author=False)

    @commands.command(name='register', help='Allows registration for a the ingame tag')
    async def register(self, ctx, tag:str, game:str):
        await ctx.reply(f'Succesfully added {tag} to the player {ctx.message.author.mention} to the {game.capitalize()} registry', mention_author=False)

    @commands.command(name='addGame', help='Adds the game as a possible candidate for scheduling and registries')
    async def addGame(self, ctx, game:str):
        with open(str(ctx.guild.id) + ".json", "r+") as f:
            flag = False
            data = json.load(f)
            payload =  {
                    'registry': {},
                    'schedule': {}
            }
            if not(str(game.lower()) in data[str(ctx.guild.id)]['games']):
                data[str(ctx.guild.id)]['games'][str(game.lower())] = payload
                f.seek(0)
                json.dump(data, f, indent=4)
                flag = True
                await ctx.reply(f'Succesfully added {game} as a possible candidate for scheduling and registries')
            else:
                await ctx.reply(f'{game.capitalize()} already exists as a possible candidate')
        
    
    @commands.command(name='removeGame', help='Adds a game to be used within scheduler commands')
    async def removeGame(self, ctx, game: str):
        with open(str(ctx.guild.id) + ".json", "r+") as f:
            flag = False
            data = json.load(f)
            if str(game.lower()) in data[str(ctx.guild.id)]['games']:
                data[str(ctx.guild.id)]['games'].pop(str(game.lower()))
                f.seek(0)
                json.dump(data, f, indent=4)
                flag = True
                await ctx.reply(f'{game.capitalize()} succesfully removed')
            else:
                await ctx.reply(f'{game.capitalize()} doesn\'t exist')


    @commands.command(name='setRegistry', help='Sets the registry channel')
    async def setRegistry(self, ctx, game:str):      
        await ctx.send(f'Successfuly set registry in {ctx.message.channel.mention} for {game.capitalize()}', delete_after=3.0)

    @commands.command(name='addSchedule', help='Schedules the game')
    async def addSchedule(self, ctx, schedule, game: str):
        await ctx.reply(f'Succesfully scheduled a game @{schedule} for {game.capitalize()}')

    @commands.command(name='removeSchedule', help='Removes scheduled item')
    async def removeSchedule(self, ctx, schedule, game: str):
        await ctx.reply(f'Succesfully unscheduled a game @{schedule} for {game.capitalize()}')