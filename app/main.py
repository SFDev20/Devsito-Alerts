import discord
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
bot = discord.Client(intents=intents)


async def load_cogs():
    for filename in os.listdir("app/commands"):
        if filename.endswith(".py"):
            extension = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
            except Exception as e:
                print(e)


async def start_all():
    await load_cogs()
    await bot.start(os.getenv("BOT_TOKEN"))

# --- Entry point ---
if __name__ == "__main__":
    asyncio.run(start_all())
