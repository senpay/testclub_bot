import discord
from discord.ext import commands
import logging
from just_config.configuration import Configuration
import json

intents=discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)
client=commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    with open ('DiscordBotMessage.json','r') as f:
        message=json.load(f)
    channel=member.guild.system_channel
    logging.info(f'{member.mention} come')
    hello_message=message["hello_message"]
    hello_message=hello_message.replace('${username}',member.mention )
    await channel.send(hello_message)

@client.event
async def on_member_remove(member):
    with open ('DiscordBotMessage.json','r') as f:
        message=json.load(f)
    channel = member.guild.system_channel
    logging.info(f'{member.mention} exit')
    traitor_message=message["traitor_message"]
    traitor_message=traitor_message.replace('${username}',member.mention )
    await channel.send(traitor_message)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx,member: discord.Member,*,reason=None):
    print("Hi")
    await ctx.send(f'Попытка кикнуть')
    await member.kick(reason=reason)
    await ctx.send(f'Succes')
    await ctx.send(f'Пользователя {member.mention} выгнали.')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     if message.content.startswith('$bot'):
#         await message.channel.send('Rо нада была, хазяин?!')

config = Configuration()

client.run(config['TOKEN'])