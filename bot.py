import os
import discord
from dotenv import load_dotenv
from connect_db import session
from common import insert_data_to_db, fetch_data

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN", "")

insert_data_to_db(session)
intents = discord.Intents.all()
client = discord.Client(command_prefix="bcs!", intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # check command.
    if message.content.startswith("bcs! part5"):
        data = fetch_data(session)
        msg = ""
        transcript = ""
        for d in data:
            transcript += f"Answer {d.id}-{d.question_number}:||**{d.transcript}**||\t"
            msg += f"\n{str(d)}\n"
        await message.channel.send(f"```\n{msg}\n```\n{transcript}")


client.run(TOKEN)
