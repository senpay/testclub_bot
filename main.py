import infrastructure.discord.discord_adapter

from flask import Flask

app = Flask(__name__)

pinged = 0


@app.route('/ping')
def ping():
    global pinged
    pinged += 1
    return f'Pong! (pinged {pinged} times)'


# if __name__ == '__main__':
#     app.run(debug=True)
