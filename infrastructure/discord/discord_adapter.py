import discord
from discord.ext import commands
from just_config.configuration import Configuration

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$bot'):
        await message.channel.send('Шо нада была, хазяин?!')

@commands.Cog.listener()
async def on_member_join(self, member):
    channel = member.guild.system_channel
    await channel.send(embed=discord.Embed(description=f'{member.mention} явился на службу.'))


config = Configuration()

client.run(config['TOKEN'])
