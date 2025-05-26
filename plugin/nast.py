from pyrogram import Client
from pyrogram.types import Message
from main import save_settings

command = "nast"

async def handler(client: Client, message: Message, args: str, settings: dict):
    if not args:
        await message.reply("╔⋞⚙️ USAGE ⚙️⋟\n║\n╠⫸ .nast times UTC+3\n║\n╚⫸⋞🌌 Cosmo 🌌⋟")
        return

    parts = args.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("╔⋞⚙️ ERROR ⚙️⋟\n║\n╠⫸ ❗ Неверный формат\n╠⫸ ✅ Пример: .nast times UTC+3\n║\n╚⫸⋞🌌 Cosmo 🌌⋟")
        return

    target, value = parts

    if target.lower() == "times":
        if not value.startswith("UTC") or len(value) < 4:
            await message.reply("╔⋞⚙️ ERROR ⚙️⋟\n║\n╠⫸ ❗ Формат: UTC±X\n╠⫸ Пример: UTC+3, UTC-5\n║\n╚⫸⋞🌌 Cosmo 🌌⋟")
            return

        try:
            offset = float(value[3:])
            if not -12 <= offset <= 14:
                await message.reply("╔⋞⚙️ ERROR ⚙️⋟\n║\n╠⫸ ❗ Смещение -12..+14\n║\n╚⫸⋞🌌 Cosmo 🌌⋟")
                return

            settings["time_timezone"] = value
            save_settings(settings)
            await message.reply(f"╔⋞⚙️ SUCCESS ⚙️⋟\n║\n╠⫸ ✅ Установлено: {value}\n║\n╚⫸⋞🌌 Cosmo 🌌⋟")
        except ValueError:
            await message.reply("╔⋞⚙️ ERROR ⚙️⋟\n║\n╠⫸ ❗ Неверное смещение\n║\n╚⫸⋞🌌 Cosmo 🌌⋟")
