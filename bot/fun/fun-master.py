import discord
from discord.ext import commands
from bot.tools import *

async def setup(bot):
    bot.add_command(eball)

@commands.command(name='8ball', help='Consults the magic 8-ball :8_ball: !8ball <Question>')
async def eball(ctx, args):
    # Gets 8ball response
        result = eightball(args)

        # Send result as embed
        if not result[0]:
            embed = discord.Embed(title="Invalid input for !8ball",
                                description=f"{result[1]}",
                                color=discord.Color.red())
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"8Ball",
                                description=f"The 8ball has spoken:\n{result[1]}",
                                color=discord.Color.green())
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
@eball.error
async def eball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title=":warning: Invalid input for !8ball",
                            description="You did not ask 8ball anything!",
                            color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)