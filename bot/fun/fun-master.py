import discord
from discord.ext import commands
from bot.tools import *

async def setup(bot):
    bot.add_command(eball)
    bot.add_command(roll)
    bot.add_command(testing_text)
    bot.add_command(dox)
    bot.add_command(flip)
    bot.add_command(harass)

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

@commands.command(name='roll', help='Rolls specified Y dice X times. !roll XdY')
async def roll(ctx, args):
    # Parse args, get result tuple
    result = roll_dice(args)
    
    # Send result as embed
    if not result[0]:
        embed = discord.Embed(title="Invalid input for !roll",
                              description=f"{result[1]}",
                              color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"Rolled dice(s)!",
                              description=f"Here are your dice rolls:\n{result[1]}",
                              color=discord.Color.green())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Invalid input for !roll",
                            description='Invalid argument!\nPlease use the format !flip X, where X is a number between 1-10',
                            color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

@commands.command(name='flip', help='Flip a coin X times. !flip X')
async def flip(ctx, args):
    # Parse args, get result tuple
    result = flip_coin(args)
    # Send result as embed
    if not result[0]:
        embed = discord.Embed(title="Invalid input for !flip",
                              description=f"{result[1]}",
                              color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"Flipped coin(s)!",
                              description=f"Here are your coinflip results:\n{', '.join(str(elem) for elem in result[1])}",
                              color=discord.Color.green())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

@commands.command(name='harass', help='Why')
async def harass(ctx):
    # Send the initial message and store the returned message object
    initial_message = await ctx.send(content=f'<@{ctx.author.id}>')

    # Create the embed
    embed = discord.Embed(title="Harass",
                          description=f'<@{ctx.author.id}>',
                          color=discord.Color.blue())

    # Edit the initial message with the embed
    await initial_message.edit(content=None, embed=embed)

@commands.command(name='whoami', help='User object information')
async def dox(ctx):
    toSend = f'{ctx.author.mention}\nGlobal_Name: {ctx.author.global_name}\nName: {ctx.author.name}\nID: {ctx.author.id}'
    await ctx.send(toSend)


@commands.command(name='ping', help='Pings the bot')
async def testing_text(ctx):
    await ctx.send("Pong")


@flip.error
async def flip_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="Empty input",
                            description="You can't flip nothing!",
                            color=discord.Color.red())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)
