import discord
from discord.ext import commands
from functions import *
import os
from dotenv import load_dotenv

load_dotenv()

description = '''
A Discord bot for my Splatoon 3 server.
It can tell you the current and next stages of regular, bankara, and coop games, 
or list the next N games on the schedule of regular, bankara, and coop games.
'''

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command(description='Examples: ?turf | ?turf 3')
async def turf(ctx, n = 2):
    if n < 1:
        messageVar = '`N` requested is too small!'
        await ctx.reply(content = messageVar)
        return
    data = get_schedule('regular', 'schedule')
    if data is None:
        await ctx.reply('Failed in getting the data!')
        return
    elif n > len(data):
        await ctx.reply('`N` requested is too large!')
        return
    elif data[0]['is_fest']:
        await ctx.reply('🎆SplatFest🎆 is going on! Use `?fest`')
        return
    messageVar = f'''
    **⤋⤋⤋ TURF WAR SCHEDULE (REQUESTED N = {n}) ⤋⤋⤋**
    '''
    await ctx.reply(content = messageVar)
    for i in range(n):
        embedVar = embed_content(data[i])
        await ctx.send(file = embedVar[0], embed = embedVar[1])

@bot.command(description='Examples: ?bankara open | ?bankara open 3 | ?bankara challenge 3')
async def bankara(ctx, format = None, n = 2):
    if n < 1:
        messageVar = '`N` requested is too small!'
        await ctx.reply(content = messageVar)
        return
    if format is None:
        messageVar = 'Please specify a BANKARA FORMAT!'
        await ctx.reply(content = messageVar)
        return
    elif format == "open":
        data = get_schedule('bankara-open', 'schedule')
        if data is None:
            await ctx.reply('Failed in getting the data!')
            return
        elif n > len(data):
            await ctx.reply('`N` requested is too large!')
            return
        elif data[0]['is_fest']:
            await ctx.reply('🎆SplatFest🎆 is going on! Use `?fest`')
            return
        messageVar = f'''
        **⤋⤋⤋ BANKARA OPEN SCHEDULE (REQUESTED N = {n}) ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        for i in range(n):
            embedVar = embed_content(data[i])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
    elif format == "challenge":
        data = get_schedule('bankara-challenge', 'schedule')
        if data is None:
            await ctx.reply('Failed in getting the data!')
            return
        elif n > len(data):
            await ctx.reply('`N` requested is too large!')
            return
        elif data[0]['is_fest']:
            await ctx.reply('🎆SplatFest🎆 is going on! GO!')
            return
        messageVar = f'''
        **⤋⤋⤋ BANKARA CHALLENGE SCHEDULE (REQUESTED N = {n}) ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        for i in range(n):
            embedVar = embed_content(data[i])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
    else:
        messageVar = 'Wrong BANKARA FORMAT!'
        await ctx.reply(content = messageVar)
        return

@bot.command(description='Examples: ?salmonrun | ?salmonrun 3')
async def salmonrun(ctx, n = 2):
    if n < 1:
        messageVar = '`N` requested is too small!'
        await ctx.reply(content = messageVar)
        return
    data = get_schedule('coop-grouping-regular', 'schedule')
    if data is None:
        await ctx.reply('Failed in getting the data!')
        return
    elif n > len(data):
        await ctx.reply('`N` requested is too large!')
        return
    messageVar = f'''
    **⤋⤋⤋ 🈺SALMON RUN🈺 SCHEDULE (REQUESTED N = {n}) ⤋⤋⤋**
    '''
    await ctx.reply(content = messageVar)
    for i in range(n):
        embedVar = embed_content_coop(data[i])
        await ctx.send(embed = embedVar)


@bot.command(description='Usage: ?now [turf|open|challenge|salmonrun|fest]')
async def now(ctx, format = None):
    data = [None] * 5
    data[0] = get_schedule('regular', 'now')
    data[1] = get_schedule('bankara-open', 'now')
    data[2] = get_schedule('bankara-challenge', 'now')
    data[3] = get_schedule('coop-grouping-regular', 'now')
    data[4] = get_schedule('fest', 'now')
    if None in data:
        await ctx.reply('Failed in getting the data!')
        return
    if format is None:
        if data[0][0]['is_fest']:
            messageVar = f'''
            **⤋⤋⤋ CURRENT 🎆SPLATFEST🎆 STAGES ⤋⤋⤋**
            '''
            await ctx.reply(content = messageVar)
            embedVar = embed_content(data[4][0])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
        else:
            messageVar = f'''
            **⤋⤋⤋ CURRENT TURF WAR STAGES ⤋⤋⤋**
            '''
            await ctx.reply(content = messageVar)
            embedVar = embed_content(data[0][0])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
            messageVar = f'''
            **⤋⤋⤋ CURRENT BANKARA OPEN STAGES ⤋⤋⤋**
            '''
            await ctx.reply(content = messageVar)
            embedVar = embed_content(data[1][0])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
            messageVar = f'''
            **⤋⤋⤋ CURRENT BANKARA CHALLENGE STAGES ⤋⤋⤋**
            '''
            await ctx.reply(content = messageVar)
            embedVar = embed_content(data[2][0])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
        messageVar = f'''
        **⤋⤋⤋ CURRENT 🈺SALMON RUN🈺 STAGE AND WEAPONS ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content_coop(data[3][0])
        await ctx.send(embed = embedVar)
    if format == 'turf':
        if data[0][0]['is_fest']:
            await ctx.reply('🎆SplatFest🎆 is going on! No regular Truf War!')
            return
        messageVar = f'''
        **⤋⤋⤋ CURRENT TURF WAR STAGES ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content(data[0][0])
        await ctx.send(file = embedVar[0], embed = embedVar[1])
    if format == 'open':
        if data[1][0]['is_fest']:
            await ctx.reply('🎆SplatFest🎆 is going on! No regular Bankara!')
            return
        messageVar = f'''
        **⤋⤋⤋ CURRENT BANKARA OPEN STAGES ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content(data[1][0])
        await ctx.send(file = embedVar[0], embed = embedVar[1])
    if format == 'challenge':
        if data[2][0]['is_fest']:
            await ctx.reply('🎆SplatFest🎆 is  going on! No regular Bankara!')
            return
        messageVar = f'''
        **⤋⤋⤋ CURRENT BANKARA CHALLENGE STAGES ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content(data[2][0])
        await ctx.send(file = embedVar[0], embed = embedVar[1])
    if format == 'salmonrun':
        messageVar = f'''
        **⤋⤋⤋ CURRENT 🈺SALMON RUN🈺 STAGE AND WEAPONS ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content_coop(data[3][0])
        await ctx.send(embed = embedVar)
    if format == 'fest':
        if not(data[4][0]['is_fest']):
            await ctx.reply('🎆SplatFest🎆 is not going on...')
            return
        messageVar = f'''
        **⤋⤋⤋ CURRENT 🎆SPLATFEST🎆 STAGES ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content(data[4][0])
        await ctx.send(file = embedVar[0], embed = embedVar[1])


@bot.command(description='Usage: ?next [turf|open|challenge|salmonrun|fest]')
async def next(ctx, format = None):
    data = [None] * 5
    data[0] = get_schedule('regular', 'next')
    data[1] = get_schedule('bankara-open', 'next')
    data[2] = get_schedule('bankara-challenge', 'next')
    data[3] = get_schedule('coop-grouping-regular', 'next')
    data[4] = get_schedule('fest', 'next')
    if None in data:
        await ctx.reply('Failed in getting the data!')
        return
    if format is None:
        if data[0][0]['is_fest']:
            messageVar = f'''
            **⤋⤋⤋ NEXT 🎆SPLATFEST🎆 STAGES ⤋⤋⤋**
            '''
            await ctx.reply(content = messageVar)
            embedVar = embed_content(data[4][0])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
        else:
            messageVar = f'''
            **⤋⤋⤋ NEXT TURF WAR STAGES ⤋⤋⤋**
            '''
            await ctx.reply(content = messageVar)
            embedVar = embed_content(data[0][0])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
            messageVar = f'''
            **⤋⤋⤋ NEXT BANKARA OPEN STAGES ⤋⤋⤋**
            '''
            await ctx.reply(content = messageVar)
            embedVar = embed_content(data[1][0])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
            messageVar = f'''
            **⤋⤋⤋ NEXT BANKARA CHALLENGE STAGES ⤋⤋⤋**
            '''
            await ctx.reply(content = messageVar)
            embedVar = embed_content(data[2][0])
            await ctx.send(file = embedVar[0], embed = embedVar[1])
        messageVar = f'''
        **⤋⤋⤋ NEXT 🈺SALMON RUN🈺 STAGE AND WEAPONS ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content_coop(data[3][0])
        await ctx.send(embed = embedVar)
    if format == 'turf':
        if data[0][0]['is_fest']:
            await ctx.reply('🎆SplatFest🎆 is going on! No regular Truf War!')
            return
        messageVar = f'''
        **⤋⤋⤋ NEXT TURF WAR STAGES ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content(data[0][0])
        await ctx.send(file = embedVar[0], embed = embedVar[1])
    if format == 'open':
        if data[1][0]['is_fest']:
            await ctx.reply('🎆SplatFest🎆 is going on! No regular Bankara!')
            return
        messageVar = f'''
        **⤋⤋⤋ NEXT BANKARA OPEN STAGES ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content(data[1][0])
        await ctx.send(file = embedVar[0], embed = embedVar[1])
    if format == 'challenge':
        if data[2][0]['is_fest']:
            await ctx.reply('🎆SplatFest🎆 is  going on! No regular Bankara!')
            return
        messageVar = f'''
        **⤋⤋⤋ NEXT BANKARA CHALLENGE STAGES ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content(data[2][0])
        await ctx.send(file = embedVar[0], embed = embedVar[1])
    if format == 'salmonrun':
        messageVar = f'''
        **⤋⤋⤋ NEXT 🈺SALMON RUN🈺 STAGE AND WEAPONS ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content_coop(data[3][0])
        await ctx.send(embed = embedVar)
    if format == 'fest':
        if not(data[4][0]['is_fest']):
            await ctx.reply('🎆SplatFest🎆 is not going on...')
            return
        messageVar = f'''
        **⤋⤋⤋ NEXT 🎆SPLATFEST🎆 STAGES ⤋⤋⤋**
        '''
        await ctx.reply(content = messageVar)
        embedVar = embed_content(data[4][0])
        await ctx.send(file = embedVar[0], embed = embedVar[1])


@bot.command(description='Examples: ?fest | ?fest 3')
async def fest(ctx, n = 2):
    if n < 1:
        messageVar = '`N` requested is too small!'
        await ctx.reply(content = messageVar)
        return
    data = get_schedule('fest', 'schedule')
    if data is None:
        await ctx.reply('Failed in getting the data!')
        return
    elif n > len(data):
        await ctx.reply('`N` requested is too large!')
        return
    elif data[0]['is_fest'] == False:
        await ctx.reply('🎆SplatFest🎆 is not going on...')
        return
    messageVar = f'''
    **⤋⤋⤋ 🎆SPLATFEST🎆 SCHEDULE (REQUESTED N = {n}) ⤋⤋⤋**
    '''
    await ctx.reply(content = messageVar)
    for i in range(n):
        embedVar = embed_content(data[i])
        await ctx.send(file = embedVar[0], embed = embedVar[1])

@bot.command(description='Example: `?archive` | `?archive 4`')
async def archive(ctx, n = None):
    pass



bot.run(os.getenv('BOT_TOKEN'))