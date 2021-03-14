import discord

from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Shows the help command, can take a name of another command to just only display that commands description')
    async def help(self, ctx, commandReq=None):
        descriptor = ''
        if commandReq:
            for cog in self.bot.cogs:
                for command in self.bot.get_cog(cog).get_commands():
                    if command.name == commandReq:
                        descriptor += f'***{cog}\n'
                        descriptor += f'**COMMAND:** {command.name},\n*{command.help}*\n\n'
                        break
        else:
            for cog in self.bot.cogs:
                descriptor += f'***{cog}***\n'
                for command in self.bot.get_cog(cog).get_commands():
                    descriptor += f'**COMMAND:** {command.name},\n*{command.help}*\n\n'

        await ctx.send(embed=discord.Embed(title='Help', description=descriptor))
