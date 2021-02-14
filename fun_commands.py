import discord

from discord.ext import commands
from databaseClient import usersDB

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', help='Used to test if the bot is functioning, responds with a pong')
    async def ping(self, ctx):
        await ctx.reply('pong', mention_author=False)

    @commands.command(name='pong', help='Used to test if the bot is functioning, responds with a pong')
    async def pong(self, ctx):
        await ctx.reply('ping', mention_author=False)

    @commands.command(name='info', help='Gives user info on their concurrent point status')
    async def info(self, ctx, *args):
        if not(args):
            response = usersDB.find_one({f'id': ctx.author.id})
            if response:
                await ctx.send(embed= await self.generateEmbed(response))
            else:
                usersDB.insert_one({'id': ctx.author.id, 'context': {'currency': 100}})
                # insert a new entry for the user, with his account balance
        else:
            pass

    async def generateEmbed(self, userData):
        user = self.bot.get_user(userData['id'])
        embed = discord.Embed(title=f"Player Card", description=str(userData['id']))
        # embed.set_image(url=user.avatar_url)
        return embed


    @commands.command(name='coinflip', help='Gives user info on their concurrent point status')
    async def coinflip(self, ctx, amount, flip):
        # coin flip gambling for virtual currency
        pass

    @commands.command(name='leaderboard', help='Shows the global leaderboard')
    async def leaderboard(self, ctx):
        # top 10 leaderboard
        pass

    @commands.command(name='donate', help='Donates points to another user')
    async def donate(self, ctx, receiver):
        # donation
        pass

    @commands.command(name='slots', help='Allows the user to play slots')
    async def slots(self, ctx, receiver):
        # allows you to play slots
        pass