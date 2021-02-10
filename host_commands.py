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
        file_name = str(ctx.guild.id) + ".json"
        with open(file_name, "r") as f:
            data = json.load(f)
        if str(game.lower()) in data['games']:
            with open(file_name, "w") as f:
                data['games'][str(game.lower())]['registry']['players'][ctx.author.id] = tag
                json.dump(data, f, indent=4)
                await ctx.reply(f'Succesfully added {tag} to the player {ctx.message.author.mention} to the {game.capitalize()} registry', mention_author=False)
        else:
            await ctx.reply(f'Couldn\'t add the user to the registry, please try correcting the game name')
            
    @commands.command(name='addGame', help='Adds the game as a possible candidate for scheduling and registries')
    async def addGame(self, ctx, game:str):
        file_name = str(ctx.guild.id) + ".json"
        with open(file_name, "r") as f:
            data = json.load(f)
        payload =  {
                'registry': {'players': {}},
                'schedule': {}
        }
        
        if not(str(game.lower()) in data['games']):
            with open(file_name, "w") as f:
                data['games'][str(game.lower())] = payload
                json.dump(data, f, indent=4)
                await ctx.reply(f'Succesfully added {game} as a possible candidate for scheduling and registries')
        else:
            await ctx.reply(f'{game.capitalize()} already exists as a possible candidate')
        
    
    @commands.command(name='removeGame', help='Adds a game to be used within scheduler commands')
    async def removeGame(self, ctx, game: str):
        file_name = str(ctx.guild.id) + ".json"
        with open(file_name, "r") as f:
            data = json.load(f)
        if str(game.lower()) in data['games']:
            with open(file_name, "w") as f:      
                data['games'].pop(str(game.lower()))
                json.dump(data, f, indent=4)
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