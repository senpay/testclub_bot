import discord
from application.members_service import MembersService, Member, Message

from just_config.configuration import Configuration

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

members_service = MembersService('temp')


@client.event
async def on_ready():
    global members_service
    members_service = MembersService(client.user.mention)
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_member_join(member):
    domain_member = Member(member.mention)
    response_msg = members_service.handle_member_joined(domain_member)
    channel=member.guild.system_channel
    await channel.send(response_msg)


@client.event
async def on_member_remove(member):
    channel=member.guild.system_channel
    domain_member = Member(member.mention)
    response_msg = members_service.handle_member_left(domain_member)
    await channel.send(response_msg)


@client.event
async def on_message(message):
    domain_message = Message(
        message.author.mention,
        message.content
    )
    response_msg = members_service.handle_message(domain_message)

    if response_msg:
        await response_msg


config = Configuration()
client.run(config['TOKEN'])
