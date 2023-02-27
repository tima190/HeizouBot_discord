import discord
from discord.ext import commands, tasks
from itertools import cycle
import random
import aiosqlite
import asyncio
import math
import sqlite3
import os


description = '''XD'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?',activity = (discord.Game("nothing")), description=description, intents=intents)



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
#database check
try:
    sqlite_connection = sqlite3.connect('database.db')
    cursor = sqlite_connection.cursor()
    print("база данных SQlite работает!")

    sqlite_select_query = "select sqlite_version();"
    cursor.execute(sqlite_select_query)
    record = cursor.fetchall()
    print("Версия базы данных SQLite: ", record)
    cursor.close()
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

@bot.event
async def on_ready():
    print(bcolors.OKGREEN + f'Logged in as {bot.user} (ID: {bot.user.id})' + bcolors.ENDC)
    print(bcolors.HEADER + f'sex ' + bcolors.ENDC + bcolors.OKCYAN + f'sex ' 
          + bcolors.ENDC + bcolors.WARNING + f'sex ' + bcolors.ENDC 
          + bcolors.FAIL + f'sex ' + bcolors.ENDC 
          + bcolors.HEADER + f'sex ' + bcolors.ENDC 
          + bcolors.OKCYAN + f'sex ' + bcolors.ENDC 
          + bcolors.WARNING + f'sex ' + bcolors.ENDC 
          + bcolors.FAIL + f'sex ☭' + bcolors.ENDC)
    print('------')
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(bcolors.OKGREEN + f"{filename} is loaded!" + bcolors.ENDC)

    setattr(bot, "db", await aiosqlite.connect("database.db"))
    #create table
    async with bot.db.cursor() as cursor:
     await cursor.execute("CREATE TABLE IF NOT EXISTS level (user INTEGER, level INTEGER, xp INTEGER, guild INTEGER)")
     await cursor.execute("CREATE TABLE IF NOT EXISTS economy (user INTEGER, money INTEGER, ticket INTEGER, guild INTEGER)")
     await bot.db.commit()

@bot.listen('on_message')
async def on_massage(massage):
    if massage.author.bot:
        return
    author = massage.author
    guild = massage.guild
    async with bot.db.cursor() as cursor:

        await cursor.execute("SELECT xp FROM level WHERE user = ? AND guild = ?", (author.id, guild.id))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM level WHERE user = ? AND guild = ?", (author.id, guild.id))
        level = await cursor.fetchone()
        if xp == None and level == None:
            await cursor.execute("INSERT INTO level (user, guild,level,xp) VALUES (?, ?, ?, ?)",(author.id,guild.id,1,0))
            await cursor.execute("SELECT xp FROM level WHERE user = ? AND guild = ?", (author.id, guild.id))
            xp = await cursor.fetchone()
            await cursor.execute("SELECT level FROM level WHERE user = ? AND guild = ?", (author.id, guild.id))
            level = await cursor.fetchone()

        xpp = xp[0]
        print(xpp)
        levell = level[0]
        print(levell)
        
        xpp += random.randint(1,5)

        needlvl = levell*30

        if xpp >= needlvl:
            xpp = xpp - needlvl
            levell += 1
        await cursor.execute("UPDATE level SET xp =? WHERE user = ? AND guild = ?", (xpp, author.id, guild.id))
        await cursor.execute("UPDATE level SET level =? WHERE user = ? AND guild = ?", (levell, author.id, guild.id))
        await bot.db.commit()
        print(f"MASSAGE -" + bcolors.HEADER + f" {massage.content}" + bcolors.ENDC + f", created by {author}, xp = {xpp} , level = {levell}")
        await cursor.execute("SELECT * FROM level")
        print(await cursor.fetchall())

@bot.command()
async def profile(ctx, member: discord.member = None):
    if member is None:
        member = ctx.author
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM level WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM level WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        level = await cursor.fetchone()

        xpp = xp[0]
        levell = level[0]

        em = discord.Embed(title=f"{member}", description=f"level = `{levell}`\n XP = `{xpp} / {levell*30}`")
        await ctx.send(embed=em)

"""@bot.command()
async def cleardb(ctx, id:int):
    async with bot.db.cursor() as cursor:
        await cursor.execute("DELETE FROM level WHERE user = ?", (int(id)))
        print(id)
        await bot.db.commit()
    print(f"{id} - был удалён из базы")"""
"""@bot.listen('on_message')
async def on_massage(massage):
    if massage.author.bot:
        return
    author = massage.author
    guild = massage.guild
    print("massage")
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id))
        level = await cursor.fetchone()

        if not xp or not level:
            await cursor.execute("INSERT INTO levels (level,xp,user,coin,gem,guild) VALUES (?, ?, ?, ?, ?, ?)",(1, 0, author.id, 0, 0, guild.id))

        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0
        
        xp += random.randint(1,5)
        await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id))
        print(f"massage by {author} - {massage.content} - xp = {xp}, level = {level}")
        demand = 10 + (level*30)
        if xp > demand:
            xp = xp - demand
            level += 1
            await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id))
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id))"""




        
    

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')




token1 = open('token.txt') # create file token.txt for your token
token2 = token1.read()
token1.close

bot.run(token2)