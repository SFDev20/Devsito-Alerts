import asyncio
from bot import start_all


async def main():
    await asyncio.gather(
        start_all()
    )

if __name__ == "__main__":
    asyncio.run(main())
