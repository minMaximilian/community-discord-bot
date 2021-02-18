import discord
import random

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
            await ctx.send(embed= await self.generateInfoEmbed(response))
        elif len(args) < 6:
            query = usersDB.find({'id': {'$in': [i.id for i in args]}})
            for i in query:
                await ctx.send(embed= await self.generateInfoEmbed(i))
        else:
            await ctx.reply(f'Can only check up to a maximum of 5 profiles')

    async def generateInfoEmbed(self, userData):
        user = await self.bot.fetch_user(userData['id'])
        embed = discord.Embed(title='Player Profile', description=f'The user profile of <@{user.id}>')
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Points', value=userData['context']['currency'])
        embed.add_field(name='Warnings', value=len(userData['context']['moderation']['warnings']))
        embed.set_footer(text=str(date.today()))
        return embed

    def generateProfile(self, userID):
        usersDB.insert_one({'id': userID, 'context': {'currency': 100, 'moderation': {'bans': 0, 'kicked': 0, 'warnings': {}}}})

    def enoughCurrency(self, userID, amount):
        result = usersDB.find_one({'id': userID})
        if result:
            if result['context']['currency'] - amount >= 0:
                return True
            else:
                return False
        else:
            self.generateProfile(userID)
            if 100 - amount >= 0:
                return True
            else:
                return False

    @commands.command(name='coinflip', help='Gives user info on their concurrent point status')
    async def coinflip(self, ctx, amount: int):
        enoughCurrency = self.enoughCurrency(ctx.author.id, amount)
        if random.choice([True, False]) and enoughCurrency:
            usersDB.update_one({'id': ctx.author.id}, {'$inc': {'context.currency': amount}})
            await ctx.reply(f'You just won {amount}')
        else:
            usersDB.update_one({'id': ctx.author.id}, {'$inc': {'context.currency': -amount}})
            await ctx.reply(f'You just lost {amount}')

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
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def warn(self, ctx, person: discord.Member, reason=None):
        payload = {'warning': reason if reason else 'No reason provided', 'date': str(date.today()), 'timestamp': int(time.time())}
        response = usersDB.find_one({'id': person.id})
        if response:
            if len(response['context']['moderation']['warnings'][str(ctx.guild.id)]) + 1 >= 3:
                usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.warnings.{ctx.guild.id}': payload}, '$inc': {f'context.moderation.kicked': 1}}, upsert=True)
                await person.kick(reason='Kicked for exceeding 3 warning limit')
                await ctx.reply(f'Succesfully kicked {person.name} for exceding 3 warning limit')
            else:
                usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.warnings.{ctx.guild.id}': payload}}, upsert=True)
            await ctx.reply(f'Succesfully warned {person.name} for Reason: \"{reason}\"')
        else:
            self.generateProfile(person.id)
            usersDB.update_one({'id': person.id}, {'$push': {f'context.moderation.warnings.{ctx.guild.id}': payload}}, upsert=True)
            await ctx.reply(f'Succesfully warned {person.name} for {reason}')

    @commands.command(name='kick', help='Usage, command @user \"Reason within these quotations\"')
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, person: discord.Member, reason=None):
        response = usersDB.find_one({'id': person.id})
        if response:
            usersDB.update_one({'id': person.id}, {'$inc': {f'context.moderation.kicked': 1}}, upsert=True)
            await person.kick(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully kicked {person.name} for Reason: {reason}')
        else:
            self.generateProfile(person.id)
            usersDB.update_one({'id': person.id}, {'$inc': {f'context.moderation.kicked': 1}}, upsert=True)
            await person.kick(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully kicked {person.name} for Reason: {reason}')

    @commands.command(name='ban', help='Usage, command @user \"Reason within these quotations\"')
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, person: discord.Member, reason=None):
        response = usersDB.find_one({'id': person.id})
        if response:
            usersDB.update_one({'id': person.id}, {'$inc': {f'context.moderation.bans': 1}}, upsert=True)
            await person.ban(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully banned {person.name} for Reason: {reason}')
        else:
            self.generateProfile(person.id)
            usersDB.update_one({'id': person.id}, {'$inc': {f'context.moderation.bans': 1}}, upsert=True)
            await person.ban(reason=(reason if reason else 'No reason'))
            await ctx.reply(f'Succesfully banned {person.name} for Reason: {reason}')

    @commands.command(name='logs', help='Usage, command @user or multiple users, under 5, returns logs of a given player and all the warnings they attained in the server')
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def logs(self, ctx, *args: discord.Member):
        if len(args) < 6:
            query = usersDB.find({'$and': [{'id': {'$in': [i.id for i in args]}}, {f'context.moderation.warnings.{ctx.guild.id}': {'$exists': True}}]})
            for i in query:
                await ctx.send(embed= await self.generateLogsEmbed(i, ctx.guild.id))
        else:
            await ctx.reply(f'Can only check up to a maximum of 5 profiles')

    async def generateLogsEmbed(self, userData, guildID):
        user = await self.bot.fetch_user(userData['id'])
        embed = discord.Embed(title='Log Profile', description=f'The logs of <@{user.id}>')
        embed.set_thumbnail(url=user.avatar_url)
        for i in userData['context']['moderation']['warnings'][str(guildID)]:
            warning = i['warning']
            dateEmbed = i['date']
            userID = i['timestamp']
            embed.add_field(name=f'Warning ID: {userID}', value=f'{warning} \n Received at:\n {dateEmbed}', inline=True)
        embed.set_footer(text=str(date.today()))
        return embed