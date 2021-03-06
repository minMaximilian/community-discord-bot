import discord

from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Shows the help command')
    async def help(self, ctx):
        descriptor = ''
        for cog in self.bot.cogs:
            descriptor += f'***{cog}***\n'
            for command in self.bot.get_cog(cog).get_commands():
                descriptor += f'**COMMAND:** {command.name},\n*{command.help}*\n\n'

        await ctx.send(embed=discord.Embed(title='Help', description=descriptor))
