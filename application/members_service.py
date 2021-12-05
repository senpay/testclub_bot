import logging
from attr import dataclass

from config.config import ON_MEMBER_LEFT_MSG, PING_COMMAND, PONG_MSG, ON_MEMBER_JOINED_MSG


@dataclass
class Member:
    name: str


@dataclass
class Message:
    author_name: str
    text: str


class MembersService:

    def __init__(self, bot_name):
        self.bot_name = bot_name

    @staticmethod
    def handle_member_left(member: Member) -> str:
        logging.info(f'{member.name} left our server. Bastard!!1')
        return ON_MEMBER_LEFT_MSG.format(member.name)

    def handle_message(self, msg) -> str:
        if msg.author_name != self.bot_name and msg.text == PING_COMMAND:
            return PONG_MSG
        return None

    @staticmethod
    def handle_member_joined(member: Member) -> str:
        logging.info(f'{member.name} joined our server. Good!!1')
        return ON_MEMBER_JOINED_MSG.format(member.name)










