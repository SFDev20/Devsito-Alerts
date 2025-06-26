import discord
import asyncio
from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


async def load_commands():
    for filename in os.listdir("app/commands"):
        if filename.endswith(".py"):
            extension = f"commands.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"[ {filename[:-3]} ]: ✔")
            except Exception as e:
                print(f"[ {filename[:-3]} ]: ✖ - {e}")


async def start_all():
    await load_commands()
    await bot.tree.sync()
    await bot.start(os.getenv("BOT_TOKEN"))

# --- Entry point ---
if __name__ == "__main__":
    asyncio.run(start_all())
