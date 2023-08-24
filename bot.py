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
import requests
import json




description = '''XD'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?',activity = (discord.Game("nothing")),help_command=None, intents=intents)

"""tenor = Tenor(token="")"""



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
     await cursor.execute('CREATE TABLE IF NOT EXISTS clan (id TEXT, name TEXT, desc TEXT, pict TEXT, level INTEGER, guild INTEGER)')
     await cursor.execute('CREATE TABLE IF NOT EXISTS userclan (id INTEGER, user INTEGER, guild INTEGER)')
     await cursor.execute('CREATE TABLE IF NOT EXISTS roles (id INTEGER, idrole INTEGER, price INTEGER)')



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

        if xpp >= needlvl:
            xpp = xpp - needlvl
            moneyy += 15*levell
            levell += 1

        if random.randint(1,2) == 1:
            moneyy += random.randint(20,50)

        if random.randint(1,20) == 1:  
            tickett += 1
            await message.add_reaction("🎟")
            token3 += 1
    
            """await massage.(f"учасник {massage.author.mention} достиг {levell} уровня!")"""
        await cursor.execute("UPDATE level SET xp =? WHERE user = ? AND guild = ?", (xpp, author.id, guild.id))
        await cursor.execute("UPDATE level SET level =? WHERE user = ? AND guild = ?", (levell, author.id, guild.id))
        await cursor.execute("UPDATE economy SET money =? WHERE user = ? AND guild = ?", (moneyy, author.id, guild.id))
        await cursor.execute("UPDATE economy SET ticket =? WHERE user = ? AND guild = ?", (tickett, author.id, guild.id))
        await bot.db.commit()
        print(bcolors.OKCYAN + "-----" + bcolors.ENDC)
        print(f"MASSAGE -" + bcolors.HEADER + f" {message.content}" + bcolors.ENDC + f", created by {author}, xp = {xpp} , level = {levell}")
        if len(message.attachments) > 0:
            print( bcolors.WARNING + f"attachment : {message.attachments}" + bcolors.ENDC )
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
            if rank == round(levell//5):
                if rank == 0:
                    ranked  = "https://i.ibb.co/Ss3f7DT/Seasonal-Rank1-1.png"
                if rank == 1:
                    ranked  = "https://i.ibb.co/hM8cCCW/Seasonal-Rank1-2.png"
                if rank == 2:
                    ranked  = "https://i.ibb.co/jD7fSQ5/Seasonal-Rank1-3.png"
                if rank == 3:
                    ranked  = "https://i.ibb.co/KF6QcKY/Seasonal-Rank1-4.png"
                if rank == 4:
                    ranked  = "https://i.ibb.co/7JN2Rp9/Seasonal-Rank1-5.png"
                if rank == 5:
                    ranked  = "https://i.ibb.co/FHk1ywz/Seasonal-Rank2-1.png"
                if rank >= 6:
                    ranked  = "https://i.ibb.co/4fL4JbX/Seasonal-Rank2-2.png"
                if rank >= 7:
                    ranked  = "https://i.ibb.co/0mMWS1p/Seasonal-Rank2-3.png"
                if rank >= 8:
                    ranked  = "https://i.ibb.co/yg1fWRD/Seasonal-Rank2-4.png"
                if rank >= 9:
                    ranked  = "https://i.ibb.co/cXGM3mc/Seasonal-Rank2-5.png"
                if rank >= 10:
                    ranked  = "https://i.ibb.co/nML7V9G/Seasonal-Rank3-1.png"
                if rank >= 11:
                    ranked  = "https://i.ibb.co/6ZQ1Krx/Seasonal-Rank3-2.png"
                if rank >= 12:
                    ranked  = "https://i.ibb.co/RD3Whj3/Seasonal-Rank3-3.png"
                if rank >= 13:
                    ranked  = "https://i.ibb.co/HtbRWR3/Seasonal-Rank3-4.png"
                if rank >= 14:
                    ranked  = "https://i.ibb.co/RD3KQ4L/Seasonal-Rank3-5.png"
                if rank >= 15:
                    ranked  = "https://i.ibb.co/LnVk2Zf/Seasonal-Rank4-1.png"
                if rank >= 16:
                    ranked  = "https://i.ibb.co/xzwKpds/Seasonal-Rank4-2.png"
                if rank >= 17:
                    ranked  = "https://i.ibb.co/GQZD20f/Seasonal-Rank4-3.png"
                if rank >= 18:
                    ranked  = "https://i.ibb.co/dWhkNgN/Seasonal-Rank4-4.png"
                if rank >= 19:
                    ranked  = "https://i.ibb.co/DfC0Ds3/Seasonal-Rank4-5.png"
                if rank >= 20:
                    ranked  = "https://i.ibb.co/55qt0C1/Seasonal-Rank5-1.png"
                if rank >= 21:
                    ranked  = "https://i.ibb.co/72Kvd7R/Seasonal-Rank5-2.png"
                if rank >= 22:
                    ranked  = "https://i.ibb.co/vP4HbW3/Seasonal-Rank5-3.png"
                if rank >= 23:
                    ranked  = "https://i.ibb.co/kqM736V/Seasonal-Rank5-4.png"
                if rank >= 24:
                    ranked  = "https://i.ibb.co/L8yqZ2F/Seasonal-Rank5-5.png"
                if rank >= 25:
                    ranked  = "https://i.ibb.co/n182k2J/Seasonal-Rank6-1.png"
                if rank >= 26:
                    ranked  = "https://i.ibb.co/BTmkccK/Seasonal-Rank6-2.png"
                if rank >= 27:
                    ranked  = "https://i.ibb.co/6v47XYS/Seasonal-Rank6-3.png"
                if rank >= 28:
                    ranked  = "https://i.ibb.co/fNQ3xH7/Seasonal-Rank6-4.png"
                if rank >= 29:
                    ranked  = "https://i.ibb.co/41ZZFFk/Seasonal-Rank6-5.png"
                if rank >= 30:
                    ranked  = "https://i.ibb.co/7tJncdC/Seasonal-Rank-Top0.png"

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
async def testing2(ctx, args, args2):
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
    if get(ctx.author.roles, id=992148541885657229):
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
    
@bot.command()
async def transfer(ctx, recipient: discord.Member, coins: int):
    author = ctx.author
    guild = ctx.guild
    sender = ctx.author
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (author.id, guild.id))
        sender_balance = await cursor.fetchone()
        # Checking if sender has enough coins to transfer
        if sender_balance is None or coins > sender_balance[0]:
            await ctx.send("Недостаточное количество зефирок для осуществления перевода.")
        else:
            # Updating sender's coin balance in the database
            sender_total = sender_balance[0] - coins
            await cursor.execute("UPDATE economy SET money = ? WHERE user = ? AND guild = ?", (sender_total, author.id, guild.id))

            # Fetching recipient's coin balance from database
            await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (recipient.id, guild.id))
            recipient_balance = await cursor.fetchone()

            # Updating recipient's coin balance in the database
            if recipient_balance is None:
                await ctx.send('нету пользователя')
            else:
                recipient_total = recipient_balance[0] + coins
                await cursor.execute("UPDATE economy SET money = ? WHERE user = ? AND guild = ?", (recipient_total, recipient.id, guild.id))
            await bot.db.commit()

            embed = discord.Embed(title="Перевод зефирок", color=discord.Color.green())
            embed.add_field(name="отправитель", value=sender.mention, inline=False)
            embed.add_field(name="получатель", value=recipient.mention, inline=False)
            embed.add_field(name="Зефирок переведено", value=str(coins), inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/QChtRvh/hyeyanksook-money.gif")
            await ctx.send(embed=embed)

@bot.command()
async def addiction(ctx, coins: int):
    author = ctx.author
    guild = ctx.guild
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (author.id, guild.id))
        sender_balance = await cursor.fetchone()
        if coins > sender_balance[0]:
            await ctx.send("Недостаточное количество зефирок.")
        else:
            sender_total = sender_balance[0] - coins
            await cursor.execute("UPDATE economy SET money = ? WHERE user = ? AND guild = ?", (sender_total, author.id, guild.id))
            win = random.randint(1,100)
            if win <= 40:
                coins_win = round(coins * 1.5)
                sender_win = sender_total + coins_win

                await cursor.execute("UPDATE economy SET money = ? WHERE user = ? AND guild = ?", (sender_win, author.id, guild.id))

                embed=discord.Embed(color=0xffff00)
                embed.add_field(name="вы выиграли ставку!", value=f"сумма выигрыша = {coins_win}", inline=False)
                embed.set_footer(text=f"текущий баланс: {sender_win}")
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(color=0xff0000)
                embed.add_field(name="вы проиграли ставку...", value="", inline=False)
                embed.set_footer(text=f"текущий баланс: {sender_total}")
                await ctx.send(embed=embed)

# ROLES



@bot.command()
async def puroles(ctx, role: int = None):
    author = ctx.author
    guild = ctx.guild
    if role == None:
        embed=discord.Embed(title="магазин ролей", color=0xff0000)
        embed.add_field(name="список цветов", value=" 1 - <@&1095968475199066173>" +
                    "\n 2 - <@&1095968171296563210>" +
                    "\n 3 - <@&1095968061015719938>" +
                    "\n 4 - <@&1095964867002904618>" +
                    "\n 5 - <@&1095964711775899698>" +
                    "\n 6 - <@&1095964532289056768>" +
                    "\n 7 - <@&1095964394053173338>" +
                    "\n 8 - <@&1095964313639976971>" +
                    "\n 9 - <@&1095964137495998474>" +
                    "\n 10 - <@&1095963735656501308>" +
                    "\n 11 - <@&1095963534594162718>" +
                    "\n каждая роль стоит 50.000"
                    , inline=False)
        await ctx.send(embed=embed) 
    else:
        async with bot.db.cursor() as cursor:
            await cursor.execute("SELECT money FROM economy WHERE user = ? AND guild = ?", (author.id, guild.id))
            sender_balance = await cursor.fetchone()
            if 50000 > sender_balance[0]:
                await ctx.send("Недостаточное количество зефирок.")
            else:
                sender_total = sender_balance[0] - 50000
                await cursor.execute("UPDATE economy SET money = ? WHERE user = ? AND guild = ?", (sender_total, author.id, guild.id))
                await cursor.execute("SELECT idrole FROM roles WHERE id = ? ", (role))
        
@bot.command()
async def give_role(ctx, role_info: str):
    with open('roles.json', 'r') as file:
        roles_data = json.load(file)
        
    try:
        role_number = int(role_info)
        role_id = roles_data.get(str(role_number))
        
        if role_id:
            role = discord.utils.get(ctx.guild.roles, id=int(role_id))
            if role:
                await ctx.author.add_roles(role)
                await ctx.send(f"You have been given the {role.name} role!")
            else:
                await ctx.send("The role does not exist.")
        else:
            await ctx.send("Invalid role number.")
            
    except ValueError:
        role_id = role_info
        role = discord.utils.get(ctx.guild.roles, id=int(role_id))
        
        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f"You have been given the {role.name} role!")
        else:
            await ctx.send("The role does not exist.")


f = open ('token.txt')
token1 = f.read()  # create file token.txt for your token

bot.run(token1)
