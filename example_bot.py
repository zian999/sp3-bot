import discord
from discord.ext import commands
from functions import *
import os
from dotenv import load_dotenv

load_dotenv()

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command(description='')
async def turf(ctx, n = 2):
    data = get_schedule('regular', 'schedule')
    if data is None:
        await ctx.send("Failed getting data!")
    data = handle(data[0])
    t = data[0]
    if datetime.now(tz = t[0].tzinfo) > t[0]:
        tdelta = timediff(datetime.now(tz = t[1].tzinfo), t[1])
        embed = discord.Embed(
            title='Turf War', description=f"Ends in {tdelta[0]} days, {tdelta[1]} hours, {tdelta[2]} mins."
        )
    else:
        tdelta = timediff(datetime.now(tz = t[0].tzinfo), t[0])
        embed = discord.Embed(
            title='Turf War', description=f"Starts in {tdelta[0]} days, {tdelta[1]} hours, {tdelta[2]} mins."
        )
    await ctx.send(embed = embed)






bot.run(os.getenv('TOKEN'))