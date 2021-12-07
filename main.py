import discord
from application.members_service import MembersService

from just_config.configuration import Configuration

from infrastructure.discord import DiscordEventListener

configuration = Configuration()

members_service = MembersService(configuration['BOT_NAME'])

intents = discord.Intents.default()
intents.members = True

client = DiscordEventListener(members_service, intents)

client.run(configuration['TOKEN'])
