import discord
import logging
from discord.ext import commands

from just_config.configuration import Configuration
import json

intents=discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    with open ('Hellomessage.json','r') as f:
        message=json.load(f)
    channel=member.guild.system_channel
    await channel.send(f'{message["1"]}{member.mention} {message["2"]}')

@client.event
async def on_member_remove(member):
    channel=member.guild.system_channel
    logging.info(f'{member.mention} exit')
    with open ('Traitormessage.json','r') as f:
        message=json.load(f)
    await channel.send(f'{message["1"]}{member.mention} {message["2"]}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$bot'):
        await message.channel.send('Rо нада была, хазяин?!')




config = Configuration()

client.run(config['TOKEN'])