import discord
from discord.ext import commands
import logging
from just_config.configuration import Configuration
import json
import repositories
from repositories import UserRepositoryDis, PostRepositoryDis
import string
import os,sqlite3

user_repository=UserRepositoryDis()
post_repository=PostRepositoryDis()
intents=discord.Intents.default()
intents.members=True
# cl = discord.Client(intents=intents)
client=commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_member_join(member):
    print('Catch event join')
    with open ('DiscordBotMessage.json','r') as f:
        message=json.load(f)
    channel=member.guild.system_channel
    logging.info(f'{member.mention} come')
    hello_message=message["hello_message"]
    hello_message=hello_message.replace('${username}',member.mention )
    await channel.send(hello_message)

@client.event
async def on_member_remove(member):
    print('Catch event exit')
    with open('DiscordBotMessage.json', 'r') as f:
        message = json.load(f)
    channel = member.guild.system_channel
    logging.info(f'{member.mention} come')
    traitor_message = message["traitor_message"]
    traitor_message = traitor_message.replace('${username}', member.mention)
    await channel.send(traitor_message)

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx,member: discord.Member,*,reason=None):
    await ctx.send(f'Попытка кикнуть')
    await member.kick(reason=reason)
    await ctx.send(f'Succes')
    await ctx.send(f'Пользователя {member.mention} выгнали.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'mag' in message.content.lower():
        if user_repository.get_user(message.author.mention)==None:
            userid=user_repository.add_user(message.author.mention)
        else:
            user=user_repository.get_user(message.author.mention)
            userid=user.id
        post_repository.add_post(message.content,userid)
        await message.channel.send('Bard word.')
    if message.content.startswith('$bot'):
        await message.channel.send('Rо нада была, хазяин?!')
    await client.process_commands(message)

config = Configuration()

client.run(config['TOKEN'])
