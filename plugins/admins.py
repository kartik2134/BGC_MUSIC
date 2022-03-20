from modules.cache.admins import admins
from modules.clientbot import call_py, bot
from pyrogram import Client, filters
from modules.design.thumbnail import thumb
from modules.clientbot.queues import QUEUE, clear_queue
from modules.helpers.filters import command, other_filters
from modules.helpers.decorators import authorized_users_only
from modules.clientbot.utils import skip_current_song, skip_item

from config import BOT_USERNAME, GROUP_SUPPORT, IMG_5
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message(command(["/reload", f"/reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "✅ **Ʌɗɱɩŋ Lɩst Uƥɗɑtɘɗ ...**"
    )


@Client.on_message(command(["Skip", "/skip", f"/skip@{BOT_USERNAME}", "/vskip"]) & other_filters)
@authorized_users_only
async def skip(c: Client, m: Message):
    await m.delete()
    user_id = m.from_user.id
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await c.send_message(chat_id, "**❌ Ɲøtɦɩŋʛ ɩs Ƈʋrrɘŋtɭy Ƥɭɑyɩŋʛ ...**")
        elif op == 1:
            await c.send_message(chat_id, "❌ Eɱƥty Qʋɘʋɘ, Lɘɑⱱɩŋʛ VƇ ...")
        elif op == 2:
            await c.send_message(chat_id, "**🗑️ Ƈɭɘɑrɩŋʛ Queues, Lɘɑⱱɩŋʛ VƇ ...**")
        else:
            buttons = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ",
                            url=f"https://t.me/{GROUP_SUPPORT}")

                ]
            ]
        )
 
            thumbnail = f"{IMG_5}"
            title = f"{op[0]}"
            image = await thumb(thumbnail, title)
            await c.send_photo(
                chat_id,
                photo=image,
                reply_markup=buttons,
                caption=f"⏭ **Sƙɩƥƥɘɗ Ɲøω Ƥɭɑyɩŋʛ » ** [{op[0]}]({op[1]})\n💭",
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "🗑 **Ʀɘɱɵⱱɘɗ Sɵŋʛ Frøɱ Qʋɘʋɘ:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["Stop", "/stop", "/stop@{BOT_USERNAME}", "End", "/end", "/end@{BOT_USERNAME}", "/vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**✅ Ɗɩsƈøŋɘƈtɘɗ Fɤøɱ VƇ ...**")
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **Ɲøtɦɩŋʛ ɩs Strɘɑɱɩŋʛ ...**")


@Client.on_message(
    command(["Pause", "/pause", "/pause@{BOT_USERNAME}", "/vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "⏸ **Ƥɑʋsɘɗ ...**"
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **Ɲøtɦɩŋʛ ɩs Strɘɑɱɩŋʛ ...**")


@Client.on_message(
    command(["Resume", "/resume", "/resume@{BOT_USERNAME}", "/vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "▶️ **Ʀɘsʋɱɘɗ ...**"
            )
        except Exception as e:
            await m.reply(f"🚫 **error:**\n\n`{e}`")
    else:
        await m.reply("❌ **Ɲøtɦɩŋʛ ɩs Strɘɑɱɩŋʛ ...**")
