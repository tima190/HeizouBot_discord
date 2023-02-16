
import discord
from discord.ext import commands
from discord import message, User
import random

token1 = open('token.txt') # create file token.txt for your token
token2 = token1.read()
token1.close

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"good started! We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('hello')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('test'):
        await message.channel.send(f'hello {message.author.id}')

    if message.content.startswith('!hug'):
        await message.channel.send(f"hugs {message.author.mention}")


client.run(str(token2))


