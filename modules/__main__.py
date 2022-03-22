import asyncio
from pytgcalls import idle
from modules.clientbot import call_py, bot, user
from pyrogram.raw.functions.bots import SetBotCommands
from pyrogram.raw.types import BotCommand, BotCommandScopeDefault


async def start_bot():
    await bot.start()
    print("[INFO]: BOT & UBOT CLIENT STARTED !!")
    await bot.send(
    SetBotCommands(
        scope=BotCommandScopeDefault(),
        lang_code="en",
        commands=[
            BotCommand(
                command="start",
                description="Start The Bot"
            ),
            BotCommand(
                command="restart", 
                description="ONLY BOT OWNER"
            ),
            BotCommand(
                command="play",
                description="Play Music As Audio"
            ),    
            BotCommand(
                command="update",
                description="ONLY BOT OWNER"
            ),
            BotCommand(
                command="vplay",
                description="Play Music As Video"
            ),
            BotCommand(
                command="skip",
                description="Skip The Current Music"
            ),
            BotCommand(
                command="pause",
                description="Pause The Current Music"
            ),
            BotCommand(
                command="resume",
                description="Resume The Paused Music"
            ),
            BotCommand(
                command="vstream",
                description="Start Live Stream"
            ),
            BotCommand(
                command="cleanup",
                description="To Clean Music Bot"
            ),
            BotCommand(
                command="join",
                description="To Invite Music Assistant"
            ),
            BotCommand(
                command="stop",
                description="Stop Playing The Music"
            ),
            BotCommand(
                command="end",
                description="End Playing The Music"
            )
        ]
    )
)
    await call_py.start()
    print("[INFO]: PY-TGCALLS CLIENT STARTED !!")
    await user.join_chat("AdityaServer")
    await user.join_chat("HeroOfficialBots")
    await user.join_chat("Yaaro_ki_yaarii")
    await user.join_chat("Modmenumaking") 
    await idle()
    print("[INFO]: STOPPING BOT & USERBOT")
    await bot.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
