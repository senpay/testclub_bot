import discord
from application.members_service import MembersService, Member, Message

from just_config.configuration import Configuration

from infrastructure.discord import DiscordEventListener

intents = discord.Intents.default()
intents.members = True

members_service = MembersService('testclub_bot') # move to configuration

client = DiscordEventListener(members_service, intents)

config = Configuration()
client.run(config['TOKEN'])
