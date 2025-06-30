from discord.ext import commands
from apscheduler.triggers.cron import CronTrigger
import httpx
from io import BytesIO
from discord import File
from PIL import Image, ImageDraw, ImageFont
import os
from utils.convertToDate import msToDate
from zoneinfo import ZoneInfo


class CountdownBanner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("GTA6_CHANNEL"))
        self.gta6_url = os.getenv("BACKGROUND_URL")
        try:
            self.bot.scheduler.add_job(
                self.sendReminder,
                CronTrigger(
                    hour=0,
                    minute=0,
                    timezone=ZoneInfo("America/Lima")
                ),
                id="gta6reminder"
            )
        except Exception:
            print("Hubo un error")

    async def getBackground(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.gta6_url)
            response.raise_for_status()
            return BytesIO(response.content)

    async def getMs(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{os.getenv('GTA6_API')}?timezone=America/Lima"
            )
            data = response.json()
            return data["miliseconds_left"]

    def editImage(self, image_bytes: BytesIO, days: int) -> BytesIO:
        image = Image.open(image_bytes).convert("RGBA")
        draw = ImageDraw.Draw(image)

        # Texto principal (grande)
        main_text = str(days)
        main_font = ImageFont.truetype(
            "resources/fonts/Rubik-Bold.ttf",
            1200
        )

        # Texto secundario (más pequeño)
        sub_text = "Dias restantes"
        sub_font = ImageFont.truetype(
            "resources/fonts/Rubik-Bold.ttf",
            250
        )

        # Obtener tamaños (bounding boxes)
        main_bbox = draw.textbbox(
            (0, 0),
            main_text,
            font=main_font,
            anchor="mm"
        )
        main_height = main_bbox[3] - main_bbox[1]

        sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font, anchor="mm")
        sub_height = sub_bbox[3] - sub_bbox[1]

        # Espacio entre textos (como gap en flex)
        spacing = 150

        # Posiciones base
        image_width, image_height = image.size
        center_x = image_width // 2
        total_height = sub_height + spacing + main_height
        start_y = (image_height - total_height) // 2

        # Dibujar texto secundario arriba
        draw.text(
            (center_x, start_y + sub_height // 2),
            sub_text,
            font=sub_font,
            fill="white",
            anchor="mm"
        )

        # Dibujar texto principal debajo
        draw.text(
            (center_x, start_y + sub_height + spacing + main_height // 2),
            main_text,
            font=main_font,
            fill="white",
            anchor="mm",
        )
        result = BytesIO()
        image.save(result, format="PNG")
        result.seek(0)
        return result

    async def sendReminder(self):
        try:
            ms = await self.getMs()
            date = msToDate(ms, True)
            channel = self.bot.get_channel(self.channel_id)
            image_bytes = await self.getBackground()
            image_bytes.seek(0)
            edit_image = self.editImage(image_bytes, date[0])
            if channel:
                message = await channel.send(
                    file=File(edit_image, filename="Reminder.jpg"),
                )
                await message.publish()
        except Exception:
            await channel.send("Hubo un error al obtener la fecha")


async def setup(bot):
    await bot.add_cog(CountdownBanner(bot))
