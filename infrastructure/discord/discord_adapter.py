import discord
import logging
<<<<<<< Updated upstream
from discord.ext import commands
=======
>>>>>>> Stashed changes
from just_config.configuration import Configuration
import json

<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
intents=discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
<<<<<<< Updated upstream
    channel=member.guild.system_channel
    await channel.send(f'Владыка {member.mention} явился!')
=======
    with open ('Hellomessage.json','r') as f:
        message=json.load(f)
    channel=member.guild.system_channel
    await channel.send(f'{message["1"]}{member.mention} {message["2"]}')
>>>>>>> Stashed changes

@client.event
async def on_member_remove(member):
    channel=member.guild.system_channel
    logging.info(f'{member.mention} exit')
<<<<<<< Updated upstream
    await channel.send(f'Владыка {member.mention} предал нас!')
=======
    with open ('Traitormessage.json','r') as f:
        message=json.load(f)
    await channel.send(f'{message["1"]}{member.mention} {message["2"]}')
>>>>>>> Stashed changes

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$bot'):
<<<<<<< Updated upstream
        print('see')
=======
>>>>>>> Stashed changes
        await message.channel.send('Rо нада была, хазяин?!')




config = Configuration()

client.run(config['TOKEN'])