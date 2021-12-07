import logging
from attr import dataclass

from config.config import ON_MEMBER_LEFT_MSG, PING_COMMAND, PONG_MSG, ON_MEMBER_JOINED_MSG


logger = logging.getLogger(__name__)

@dataclass
class Member:
    name: str


@dataclass
class Message:
    author_name: str
    text: str
    channel_name: str


class MessageSender:

    def send_to_general(self, message: str):
        raise NotImplementedError()

    def send_to_channel_name(self, channel_name: str, message: str):
        raise NotImplementedError()


class MembersService:

    def __init__(self, bot_name: str, message_sender: MessageSender):
        self.bot_name = bot_name
        self.message_sender = message_sender

    @staticmethod
    def handle_member_left(member: Member) -> str:
        logger.info(f'{member.name} left our server. Bastard!!1')
        return ON_MEMBER_LEFT_MSG.format(member.name)

    def handle_message(self, msg: Message):
        if msg.author_name != self.bot_name and msg.text == PING_COMMAND:
            return self.message_sender.send_to_channel_name(msg.channel_name, PONG_MSG)
        return None

    @staticmethod
    def handle_member_joined(member: Member) -> str:
        logger.info(f'{member.name} joined our server. Good!!1')
        return ON_MEMBER_JOINED_MSG.format(member.name)










