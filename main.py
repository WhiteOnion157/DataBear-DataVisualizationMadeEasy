from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, File
from graphing import create_graph

#Load .env Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#Required Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

async def check_csv(message):
    # Currently, only csv files are accepted, so we dont respond if a file isnt a csv
    for i in range(len(message.attachments)): 
        if not message.attachments[i].filename.endswith('.csv'):
            return False
    return True

#Startup for bot
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running')

#Incoming Message
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        #Bot is the one who wrote the message
        return
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    # Logging message
    print(f'[{channel}] {username}: "{user_message}"')
    if check_csv(message):
        await create_graph(message)

def main() -> None:
    client.run(token = TOKEN)

if __name__ == '__main__':
    main()
