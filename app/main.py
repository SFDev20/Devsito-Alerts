import discord
import asyncio
from dotenv import load_dotenv
import os
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.scheduler = AsyncIOScheduler()


async def load_commands():
    for filename in os.listdir("app/commands"):
        if filename.endswith(".py"):
            extension = f"commands.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"[ Command ] {filename[:-3]}: ✔")
            except Exception as e:
                print(f"[ Command ] {filename[:-3]}: ✖ - {e}")


async def load_events():
    for filename in os.listdir("app/events"):
        if filename.endswith(".py"):
            extension = f"events.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"[ Event ] {filename[:-3]}: ✔")
            except Exception as e:
                print(f"[ Event ] {filename[:-3]}: ✖ - {e}")


async def load_tasks():
    for filename in os.listdir("app/tasks"):
        if filename.endswith(".py"):
            extension = f"tasks.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"[ Task ] {filename[:-3]}: ✔")
            except Exception as e:
                print(f"[ Task ] {filename[:-3]}: ✖ - {e}")


async def start_all():
    await load_commands()
    await load_events()
    await load_tasks()
    await bot.start(os.getenv("BOT_TOKEN"))

# --- Entry point ---
if __name__ == "__main__":
    asyncio.run(start_all())
