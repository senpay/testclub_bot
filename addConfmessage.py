

from repositories import Confmesss


Confmessages=Confmesss()




ON_MEMBER_LEFT_MSG = "{} оказался пердателем!"
Confmessages.add_post(ON_MEMBER_LEFT_MSG, "ON_MEMBER_LEFT_MSG")
PONG_MSG = 'Шо нада была, хазяин?!'
Confmessages.add_post(PONG_MSG, "PONG_MSG")
PING_COMMAND = '$bot'
Confmessages.add_post(PING_COMMAND, "PING_COMMAND")
ON_MEMBER_JOINED_MSG = """{}, Привет!
Я - бот Test Club'a.
Test Club был создан Александром Пушкаревым (он же Дядя Саша) и на его канале на ютубе ты найдешь много полезной информации.
Рекомендуем подписаться на канал и просмотреть плейлисты:
В общем, добро пожаловать в клуб!
"""
Confmessages.add_post(ON_MEMBER_JOINED_MSG, "ON_MEMBER_JOINED_MSG")