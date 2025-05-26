import os
import json
from pyrogram import Client, filters, idle
from pyrogram.types import Message

# Отключаем логирование
import logging
logging.getLogger().setLevel(logging.ERROR)

COMMAND_PREFIXES = [".l", "azi", ".tlp", "!"]
SETTINGS_FILE = "conf.json"

def load_settings():
    default = {"time_timezone": "UTC+3"}
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return {**default, **json.load(f)}
        except:
            return default
    return default

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

settings = load_settings()
os.makedirs("plugin", exist_ok=True)

app = Client("cub_bot", api_id=21004939, api_hash="05b2b4afbae9aecfd3dfd34893afff6f")

def load_commands():
    commands = {}
    for filename in os.listdir("plugin"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                module = __import__(f"plugin.{filename[:-3]}", fromlist=["*"])
                if hasattr(module, "command") and hasattr(module, "handler"):
                    commands[module.command] = module.handler
            except Exception as e:
                print(f"⚠️ Ошибка загрузки модуля {filename}: {e}")
    return commands

commands = load_commands()

@app.on_message(filters.private | filters.group)
async def handle_commands(client: Client, message: Message):
    text = message.text or message.caption
    if not text: return
    
    prefix = next((p for p in COMMAND_PREFIXES if text.startswith(p)), None)
    if not prefix: return
    
    cmd_part = text[len(prefix):].strip()
    if not cmd_part: return
    
    command = cmd_part.split()[0].lower()
    args = cmd_part[len(command):].strip()

    if command in commands:
        try:
            await commands[command](client, message, args, settings)
        except Exception as e:
            await message.reply(f"╔⋞⚙️ ERROR ⚙️⋟\n║\n╠⫸ ❗ {e}\n║\n╚⫸⋞🌌 Cosmo 🌌⋟")

async def send_startup_message():
    welcome_msg = """✅ CUB запущен на вашей странице.
---------------------------------------
💕 Благодарим за доверие, и использование нашего проекта.
😇 Приятного тебе использования.
---------------------------------------
❗То что нужно знать :
⚠️ Перед командами должен ставится префикс
ℹ️ Ваши префиксы: """ + ", ".join(COMMAND_PREFIXES) + """
📖 Списочек команд: (ваш список команд)
---------------------------------------
🔗 Наш канал в Telegram: https://t.me/cosmo_projects
😎 Разработчики проекта:
Mavi Cosmo
Mavan Shewyakov
---------------------------------------
💙 С любовью Cosmo Project"""
    
    print(welcome_msg)
    await app.send_message("me", welcome_msg)

async def main():
    await app.start()
    await send_startup_message()
    await idle()

if __name__ == "__main__":
    app.run(main())
