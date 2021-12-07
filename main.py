import discord
import logging
from application.members_service import MembersService

from just_config.configuration import Configuration

from infrastructure.discord import DiscordEventListener, DiscordMessageSender


log_format = (
    '[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')

logging.basicConfig(
    level='CRITICAL',
    format=log_format
)

logging.getLogger('infrastructure.discord').setLevel('INFO')
logging.getLogger('application.members_service').setLevel('INFO')

configuration = Configuration()

intents = discord.Intents.default()
intents.members = True

discord_message_sender = DiscordMessageSender(None)

members_service = MembersService(configuration['BOT_NAME'], discord_message_sender)

client = DiscordEventListener(members_service, intents)
discord_message_sender.client = client
client.run(configuration['TOKEN'])
