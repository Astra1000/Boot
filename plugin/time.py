from datetime import datetime, timezone, timedelta
from pyrogram import Client
from pyrogram.types import Message

command = "time"

async def handler(client: Client, message: Message, args: str, settings: dict):
    try:
        tz_str = settings.get("time_timezone", "UTC+3")
        offset = timedelta(hours=float(tz_str[3:]))
        
        current = datetime.now(timezone(offset))
        response = f"""╔⋞⏳ TIME INFO ⏳⋟
║
╠⫸ 📅 День недели: {current.strftime("%A")}
╠⫸ 🗓 Дата: {current.strftime("%d.%m.%Y")}
╠⫸ 🕒 Время: {current.strftime("%H:%M:%S")}
╠⫸ 🌏 Временная зона: {tz_str}
║
╚⫸⋞🌌 Cosmo 🌌⋟"""
        await message.reply(response)
    except Exception as e:
        await message.reply(f"╔⋞⚙️ ERROR ⚙️⋟\n║\n╠⫸ ❗ {e}\n║\n╚⫸⋞🌌 Cosmo 🌌⋟")
