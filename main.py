import infrastructure.discord.discord_adapter

from flask import Flask

app = Flask(__name__)

pinged = 0

@app.route('/ping')
def ping():
    pinged += 1
    return f'Pong! (pinged {pinged} times)'
