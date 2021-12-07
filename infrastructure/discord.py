import discord

from application.members_service import MembersService, Member, Message


class DiscordEventListener(discord.Client):

    def __init__(self, members_service: MembersService, intents: discord.Intents):
        super(DiscordEventListener, self).__init__(intents=intents)
        self.members_service = members_service

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_member_join(self, member):
        domain_member = Member(member.mention)
        response_msg = self.members_service.handle_member_joined(domain_member)
        general_channel = member.guild.system_channel
        await general_channel.send(response_msg)

    async def on_member_remove(self, member):
        domain_member = Member(member.mention)
        response_msg = self.members_service.handle_member_left(domain_member)
        general_channel = member.guild.system_channel
        await general_channel.send(response_msg)

    async def on_message(self, message):
        domain_message = Message(
            message.author.mention,
            message.content
        )
        response_msg = self.members_service.handle_message(domain_message)

        if response_msg:
            message_channel = message.channel
            await message_channel.send(response_msg)
