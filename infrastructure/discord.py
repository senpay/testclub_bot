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
        channel = member.guild.system_channel
        await channel.send(response_msg)

    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        domain_member = Member(member.mention)
        response_msg = self.members_service.handle_member_left(domain_member)
        await channel.send(response_msg)

    async def on_message(self, message):
        channel = message.channel
        domain_message = Message(
            message.author.mention,
            message.content
        )
        response_msg = self.members_service.handle_message(domain_message)

        if response_msg:
            await channel.send(response_msg)
