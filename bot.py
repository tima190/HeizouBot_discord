
import discord

token1 = open('token.txt') # create file token.txt for your token
token2 = token1.read()
token1.close

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$give zephir'):
        await message.channel.send('бля чел)')

client.run(str(token2))

@client.event
async def on_ready():
    print()
