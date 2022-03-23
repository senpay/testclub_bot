import asyncio
import logging

import discord
from discord import utils, Client

from application.members_service import MembersService, Member, Message, MessageSender

logger = logging.getLogger(__name__)


class DiscordMessageSender(MessageSender):

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

    def send_to_user(self, user: str, message: str):
        self._send_to_user(user, message)

    @staticmethod
    def _send_to_channel(channel: discord.TextChannel, message: str):
        if not channel:
            logger.warning("Can't send anything, wasn't properly set up yet")
            return None
        asyncio.create_task(channel.send(message))

    @staticmethod
    def _send_to_user(user: Member, message: str):
        if not user:
            logger.warning("Can't send anything, wasn't properly set up yet")
            return None
        asyncio.create_task(user.send(message))

    def _get_channel_by_name(self, name: str) -> str:
        if not self.client:
            logger.warning(f"Can't find channel {name}, wasn't properly set up yet")
            return None
        text_channels = [x for x in self.client.get_all_channels()]
        return utils.get(text_channels, name=name)


class DiscordEventListener(discord.Client):

    def __init__(self, members_service: MembersService, intents: discord.Intents):
        super(DiscordEventListener, self).__init__(intents=intents)
        self.members_service = members_service

    async def on_ready(self):
        logger.info('We have logged in as {0.user}'.format(self))

    async def on_member_join(self, member):
        domain_member = Member(member.mention)
        self.members_service.handle_member_joined(domain_member)

    async def on_member_remove(self, member):
        domain_member = Member(member.mention)
        self.members_service.handle_member_left(domain_member)

    async def on_message(self, message):
        domain_message = Message(
            message.author.mention,
            message.content,
            message.channel.name
        )
        self.members_service.handle_message(domain_message)
