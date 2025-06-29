from discord.ext import commands


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.synced = False

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.synced:
            await self.bot.tree.sync()
            self.synced = True
        self.bot.scheduler.start()
        print(f"Bot ready as {self.bot.user}")


async def setup(bot):
    await bot.add_cog(Ready(bot))
