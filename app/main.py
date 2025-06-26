import discord
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
bot = discord.Client(intents=intents)


async def start_all():
    await bot.start(os.getenv("BOT_TOKEN"))

# --- Entry point ---
if __name__ == "__main__":
    asyncio.run(start_all())
