import discord

from discord.ext import commands
from databaseClient import usersDB
from datetime import date
import time

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
    @commands.guild_only()
    async def info(self, ctx, *args: discord.Member):
        if not(args):
            response = usersDB.find_one({'id': ctx.author.id})
            if not(response):
                self.generateProfile(ctx.author.id)
                response = usersDB.find_one({f'id': ctx.author.id})
            await ctx.send(embed= await self.generateEmbed(response))
        elif len(args) < 6:
            query = usersDB.find({'id': {'$in': [i.id for i in args]}})
            for i in query:
                await ctx.send(embed= await self.generateEmbed(i))
        else:
            await ctx.reply(f'Can only check up to a maximum of 5 profiles')

    async def generateEmbed(self, userData):
        user = await self.bot.fetch_user(userData['id'])
        embed = discord.Embed(title='Player Profile', description=f'The user profile of <@{user.id}>')
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Points', value=userData['context']['currency'])
        embed.add_field(name='Warnings', value=len(userData['context']['moderation']['warnings']))
        embed.set_footer(text=str(date.today()))
        return embed

    def generateProfile(self, id):
        usersDB.insert_one({'id': id, 'context': {'currency': 100, 'moderation': {'bans': 0, 'kicked': 0, 'warnings': {}}}})

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
    
    @commands.command(name='warn', help='Usage, command @user \"Reason within these quotations\", kicks the user after 3 strikes')
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def warn(self, ctx, person: discord.Member, reason=None):
        payload = {'warning': reason if reason else 'No reason provided', 'date': str(date.today()), 'timestamp': str(time.time())}
        response = usersDB.find_one({'id': person.id})
        if response:
            usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.warnings.{ctx.guild.id}': payload}}, upsert=True)
            if len(response['context']['moderation']['warnings'][str(ctx.guild.id)]) + 1 >= 3:
                await person.kick(reason='Kicked for exceeding 3 warning limit')
                await ctx.reply(f'Succesfully kicked {person.name} for exceding 3 warning limit')
            await ctx.reply(f'Succesfully warned {person.name} for Reason: \"{reason}\"')
        else:
            self.generateProfile(person.id)
            usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.warnings.{ctx.guild.id}': payload}}, upsert=True)
            await ctx.reply(f'Succesfully warned {person.name} for {reason}')
