import asyncio
import logging

import discord
from discord import utils, Client, Member

from config.config import ON_MEMBER_JOINED_MSG, ON_MEMBER_LEFT_MSG, PING_COMMAND, PONG_MSG

logger = logging.getLogger(__name__)


class DiscordMessageSender:

    def __init__(self, client: Client):
        self.client = client
        self.__general_channel = None

    @property
    def general_channel(self):
        if not self.__general_channel:
            self.__general_channel = self._get_channel_by_name('general')
        return self.__general_channel

    def send_to_general(self, message: str):
        self._send_to_channel(self.general_channel, message)

    def send_to_channel_name(self, channel_name: str, message: str):
        channel = self._get_channel_by_name(channel_name)
        self._send_to_channel(channel, message)

    def send_to_user(self, member: Member, message: str):
        self._send_to_user(member, message)

    @staticmethod
    def _send_to_channel(channel: discord.TextChannel, message: str):
        if not channel:
            logger.warning("Can't send anything, wasn't properly set up yet")
            return None
        asyncio.create_task(channel.send(message))

    @staticmethod
    def _send_to_user(member: Member, message: str):
        if not member:
            logger.warning("Can't send anything, wasn't properly set up yet")
            return None
        asyncio.create_task(member.send(message))

    def _get_channel_by_name(self, name: str) -> str:
        if not self.client:
            logger.warning(f"Can't find channel {name}, wasn't properly set up yet")
            return None
        text_channels = [x for x in self.client.get_all_channels()]
        return utils.get(text_channels, name=name)


class DiscordEventListener(discord.Client):

    def __init__(self, message_sender: DiscordMessageSender, intents: discord.Intents, bot_name: str):
        super(DiscordEventListener, self).__init__(intents=intents)
        self.message_sender = message_sender
        self.bot_name = bot_name

    async def on_ready(self):
        logger.info('We have logged in as {0.user}'.format(self))

    async def on_member_join(self, member):
        self.message_sender.send_to_user(member, ON_MEMBER_JOINED_MSG.format(member.name))
        logger.info(f'{member.name} has joined to our server. He/She on the right way!!!')

    async def on_member_remove(self, member):
        self.message_sender.send_to_general(ON_MEMBER_LEFT_MSG.format(member.mention))
        logger.info(f'{member.name} left our server. Bastard!!1')

    async def on_message(self, message):
        if message.author.mention != self.bot_name and message.content == PING_COMMAND:
            self.message_sender.send_to_channel_name(message.channel.name, PONG_MSG)
