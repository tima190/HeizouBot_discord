import discord
from discord import ChannelType, Embed, Member, Object
from discord.ext import commands, tasks
from itertools import cycle
import random
import aiosqlite
import asyncio
import math
import sqlite3
import os
import re
from discord.utils import get
import schedule    
import time
import uuid

"""os.startfile(r"clear.py")"""


description = '''XD'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?',activity = (discord.Game("nothing")),help_command=None, intents=intents)



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
     await cursor.execute('CREATE TABLE IF NOT EXISTS daily (user INTEGER, ch INTEGER, coun INTEGER, guild INTEGER)')
     await cursor.execute('CREATE TABLE IF NOT EXISTS clan (id TEXT, name TEXT, desc TEXT, level INTEGER, xp INTEGER, prit INTEGER, guild INTEGER)')
     await cursor.execute('CREATE TABLE IF NOT EXISTS userclan (id INTEGER, user INTEGER, guild INTEGER)')


@bot.listen('on_message')
async def on_massage(message):
    token3 = 0
    if message.author.bot:
        return
    author = message.author
    if message.content.startswith("?"):
        return
    guild = message.guild
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

        #economy

        await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (author.id, guild.id))
        money = await cursor.fetchone()
        await cursor.execute("SELECT ticket FROM economy WHERE user = ? AND guild = ?", (author.id, guild.id))
        ticket = await cursor.fetchone()
        if money == None and ticket == None:
            await cursor.execute("INSERT INTO economy (user,guild,money,ticket) VALUES (?, ?, ?, ?)",(author.id,guild.id,0,0))
            await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (author.id, guild.id))
            money = await cursor.fetchone()
            await cursor.execute("SELECT ticket FROM economy WHERE user = ? AND guild = ?", (author.id, guild.id))
            ticket = await cursor.fetchone()

        xpp = xp[0]

        levell = level[0]

        moneyy = money[0]

        tickett = ticket[0]

        
        xpp += random.randint(1,5)

        needlvl = (20+(10*levell))
        print(needlvl)

        if xpp >= needlvl:
            xpp = xpp - needlvl
            moneyy += 15*levell
            levell += 1

        if random.randint(1,2) == 1:
            moneyy += random.randint(20,50)

        if random.randint(1,20) == 1:  
            tickett += 1
            await message.add_reaction("🈵")
            token3 += 1
    
            """await massage.(f"учасник {massage.author.mention} достиг {levell} уровня!")"""
        await cursor.execute("UPDATE level SET xp =? WHERE user = ? AND guild = ?", (xpp, author.id, guild.id))
        await cursor.execute("UPDATE level SET level =? WHERE user = ? AND guild = ?", (levell, author.id, guild.id))
        await cursor.execute("UPDATE economy SET money =? WHERE user = ? AND guild = ?", (moneyy, author.id, guild.id))
        await cursor.execute("UPDATE economy SET ticket =? WHERE user = ? AND guild = ?", (tickett, author.id, guild.id))
        await bot.db.commit()
        print(f"MASSAGE -" + bcolors.HEADER + f" {message.content}" + bcolors.ENDC + f", created by {author}, xp = {xpp} , level = {levell}")
        await cursor.execute("SELECT * FROM level")
        print(author.id)
        if token3 == 1:
            print(bcolors.OKGREEN + "token gived!" + bcolors.ENDC)

@bot.command()
async def profile(ctx, member: Member = None):
    if member is None:
        member = ctx.author
    
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM level WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM level WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        level = await cursor.fetchone()
        await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        money = await cursor.fetchone()
        await cursor.execute("SELECT ticket FROM economy WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        ticket = await cursor.fetchone()

        if money == None and ticket == None:
            await cursor.execute("INSERT INTO economy (user,guild,money,ticket) VALUES (?, ?, ?, ?)",(member.id, ctx.guild.id,0,0))
            await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
            money = await cursor.fetchone()
            await cursor.execute("SELECT ticket FROM economy WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
            ticket = await cursor.fetchone()

        xpp = xp[0]
        levell = level[0]
        moneyy = money[0]
        tickett = ticket[0]

        print(xpp,levell,moneyy,tickett)

        ranked = None

        for rank in range (0,7):
            if rank == round(levell//10):
                if rank == 0:
                    ranked  = "https://i.ibb.co/Ss3f7DT/Seasonal-Rank1-1.png"
                if rank == 1:
                    ranked  = "https://i.ibb.co/4fL4JbX/Seasonal-Rank2-2.png"
                if rank == 2:
                    ranked  = "https://i.ibb.co/RD3Whj3/Seasonal-Rank3-3.png"
                if rank == 3:
                    ranked  = "https://i.ibb.co/dWhkNgN/Seasonal-Rank4-4.png"
                if rank == 4:
                    ranked  = "https://i.ibb.co/L8yqZ2F/Seasonal-Rank5-5.png"
                if rank == 5:
                    ranked  = "https://i.ibb.co/41ZZFFk/Seasonal-Rank6-5.png"
                if rank >= 6:
                    ranked  = "https://i.ibb.co/x6ZQ3qd/Seasonal-Rank7-5.png"

        em = discord.Embed(title=f"{member}", description=f"level = `{levell}`\n XP = `{xpp} / {20+(10*levell)}`\nzephyr = `{moneyy}`\nticket = `{tickett}`")
        em.set_thumbnail(url=ranked)
        await ctx.send(embed=em)

@bot.command()
async def guild_create(ctx, name):
    author = ctx.author
    guild = ctx.guild
    uui = (str(uuid.uuid4()))
    print(type(uui))
    print(uui)
    await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (author.id, guild.id))
    money = await cursor.fetchone()
    money = money[0]
    if money > 20000:
        money -= 20000
    
    



@bot.command()
async def testing(ctx, args, args2):
    await ctx.send(f"1 часть - {args}, 2 часть - {args2}")
    uui = (str(uuid.uuid4()))
    print(type(uui))
    print(uui)

@bot.command()
@commands.cooldown(1, 60*60*12, commands.BucketType.user)
async def daily(ctx):
    dailym = 0
    author = ctx.author
    guild = ctx.guild
    money = 0
    async with bot.db.cursor() as cursor:
        await bot.db.commit()
        await cursor.execute("SELECT ch FROM daily WHERE user = ? AND guild = ?", (author.id, ctx.guild.id))
        check = await cursor.fetchone()
        await cursor.execute("SELECT coun FROM daily WHERE user = ? AND guild = ?", (author.id, ctx.guild.id))
        count1 = await cursor.fetchone()
        await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (author.id, ctx.guild.id))
        money = await cursor.fetchone()
        if check == None or count1 == None:
            await cursor.execute("INSERT INTO daily (user,guild,ch,coun) VALUES (?, ?, ?, ?)",(author.id,guild.id,1,0))
            await cursor.execute("SELECT ch FROM daily WHERE user = ? AND guild = ?", (author.id, ctx.guild.id))
            check = await cursor.fetchone()
            await cursor.execute("SELECT coun FROM daily WHERE user = ? AND guild = ?", (author.id, ctx.guild.id))
            count1 = await cursor.fetchone()
        checkk = check[0]
        count2 = count1[0]
        moneyy = money[0]
        print(count2)
        if dailym == 0:
           checkk = 0
           count2 += 1
           dailym = random.randint(200,400)
           money = moneyy + dailym
           embed=discord.Embed(title="Ежедневная награда", description="вы получили ежедневную награду!", color=0x00ff40)
           embed.set_thumbnail(url="https://i.ibb.co/PtQCBDX/1052717040403763242.png")
           embed.add_field(name=f"{dailym} зефирки", value=f"{count2} раз вы использовали команду", inline=True)
           embed.set_footer(text="через 12 часов вы сможете использовать ещё раз")
           await ctx.send(embed=embed)

           await cursor.execute("UPDATE daily SET ch =? WHERE user = ? AND guild = ?", (checkk, author.id, guild.id))
           await cursor.execute("UPDATE daily SET coun =? WHERE user = ? AND guild = ?", (count2, author.id, guild.id))
           await cursor.execute("UPDATE economy SET money =? WHERE user = ? AND guild = ?", (money, author.id, guild.id))
           await bot.db.commit()
           print(checkk)
           print(count2)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(f"такой команды нету 😏")
        await asyncio.sleep(1)
        delete = await ctx.channel.purge(limit=1)
    if isinstance(error, commands.CommandOnCooldown):
        cd = round(error.retry_after)
        hours = str(cd // 3600)
        minutes = str(cd % 60)
        await ctx.send(f"у вас кулдаун, отдохните) \nподождите {hours} часов и {minutes} минут")
    
@bot.command()
async def cleard(ctx):
    if get(ctx.author.roles, id=1000443041762512896):
        async with bot.db.cursor() as cursor:
            await cursor.execute("UPDATE daily SET ch =1")
            await bot.db.commit()
            await ctx.send("daily сброшены")
        

@bot.command()
async def topz(ctx):
    A = None
    B = None
    X = [0]*5
    countmembers = 0
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT money FROM economy ORDER BY money DESC")
      A = await cursor.fetchall()
      chars = [')', '(', ',']
      await cursor.execute("SELECT user FROM economy ORDER BY money DESC")
      B = await cursor.fetchall()
 
      for guild in bot.guilds:
         for member in guild.members:
          countmembers += 1
      for i in range (5):
          X[i] = A[i]
          X[i] = str(X[i])
          X[i] = re.sub('[(),]', '', X[i])
      for i in range (5):
          B[i] = str(B[i])
          B[i] = re.sub('[(),]', '', B[i])
          B[i] = int(B[i])
          B[i] = await bot.fetch_user(B[i])
      await ctx.send(f"top of zepfyr\n1.{X[0]}, {B[0]}\n2.{X[1]}, {B[1]}\n3.{X[2]}, {B[2]}\n4.{X[3]}, {B[3]}\n5.{X[4]}, {B[4]}\n \nколичество участников на сервере = {countmembers}")

      
      em = discord.Embed(
          title="top",
          description="of zephyr"
          )
      """em = Embed.add_field"""
      print(countmembers)
    
@bot.command()
async def topl(ctx):
    A = None
    B = None
    X = [0]*5
    countmembers = 0
    async with bot.db.cursor() as cursor:
      await cursor.execute("SELECT level FROM level ORDER BY level DESC")
      A = await cursor.fetchall()
      chars = [')', '(', ',']
      await cursor.execute("SELECT user FROM level ORDER BY level DESC")
      B = await cursor.fetchall()
 
      for guild in bot.guilds:
         for member in guild.members:
          countmembers += 1
      for i in range (5):
          X[i] = A[i]
          X[i] = str(X[i])
          X[i] = re.sub('[(),]', '', X[i])
      for i in range (5):
          B[i] = str(B[i])
          B[i] = re.sub('[(),]', '', B[i])
          B[i] = int(B[i])
          B[i] = await bot.fetch_user(B[i]) 
      await ctx.send(f"top of zepfyr\n1.{X[0]}, {B[0]}\n2.{X[1]}, {B[1]}\n3.{X[2]}, {B[2]}\n4.{X[3]}, {B[3]}\n5.{X[4]}, {B[4]}\n \nколичество участников на сервере = {countmembers}")

      em = discord.Embed(
          title="top",
          description="of zephyr"
          )
      """em = Embed.add_field"""
      print(countmembers)

@bot.command(aliases=['Ban'])
async def ban(ctx, member: Member=None, *, reason=None):
    print(member)
    print(reason)
    if get(ctx.author.roles, id=1038682492137377844):
        if member is None:
            await ctx.send(f"укажите негодяя, которого забанить")
        else:
            if reason != None:
             await ctx.guild.ban(member)
             await ctx.send(f"{member.mention} отправился в азкаБАН НА ВЕКИ ВЕЧНЫЕ\nзабанил - {ctx.author.mention}\nпричина - ```{reason}```")  
            if reason is None:
             await ctx.guild.bam(member)
             await ctx.send(f"{member.mention} отправился в азкаБАН НА ВЕКИ ВЕЧНЫЕ\nзабанил - {ctx.author.mention}")  
        
    else:
        await ctx.send(f"у вас нет прав на бан участников")



token1 = open('token.txt') # create file token.txt for your token
token2 = token1.read()
token1.close

bot.run(token2)