import discord
import logging
from discord.ext import commands
from just_config.configuration import Configuration


intents=discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    channel=member.guild.system_channel
    await channel.send(f'Владыка {member.mention} явился!')

@client.event
async def on_member_remove(member):
    channel=member.guild.system_channel
    logging.info(f'{member.mention} exit')
    await channel.send(f'Владыка {member.mention} предал нас!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$bot'):
        print('see')
        await message.channel.send('Rо нада была, хазяин?!')




config = Configuration()

client.run(config['TOKEN'])