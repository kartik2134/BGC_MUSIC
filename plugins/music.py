from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from modules.design.thumbnail import thumb
from modules.helpers.filters import command, other_filters
from modules.clientbot.queues import QUEUE, add_to_queue
from modules.clientbot import call_py, user
from modules.clientbot.utils import bash
from config import BOT_USERNAME, IMG_5, BOT_NAME, GROUP_SUPPORT
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link: str):
    stdout, stderr = await bash(
        f'yt-dlp -g -f "best[height<=?720][width<=?1280]" {link}'
    )
    if stdout:
        return 1, stdout
    return 0, stderr


@Client.on_message(command(["Play", "@", "/p", "/play", "/play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    if m.sender_chat:
        return await m.reply_text(
            "you're an __Anonymous__ user !\n\n» revert back to your real user account to use this bot."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 To use me, I need to be an **Administrator** with the following **permissions**:\n\n» ❌ __Invite users__\n\nOnce done, type /reload"
        )
        return
    if not a.can_invite_users:
        await m.reply_text(
            "💡 To use me, Give me the following permission below:"
            + "\n\n» ❌ __Add users__\n\nOnce done, try again."
        )
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await c.unban_chat_member(chat_id, ubot)
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
    except UserNotParticipant:
        try:
            invitelink = await c.export_chat_invite_link(chat_id)
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            return await m.reply_text(
                f"❌ **userbot failed to join**\n\n**reason**: `{e}`"
            )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **Ɗøωŋɭøɑɗɩŋʛ ...**")
            dl = await replied.download()
            link = replied.link
            
            try:
                if replied.audio:
                    songname = replied.audio.title[:70]
                    songname = replied.audio.file_name[:70]
                    duration = replied.audio.duration
                elif replied.voice:
                    songname = "Voice Note"
                    duration = replied.voice.duration
            except BaseException:
                songname = "Audio"
            
            if chat_id in QUEUE:
                title = songname
                userid = m.from_user.id
                thumbnail = f"{IMG_5}"
                image = await thumb(thumbnail, title, userid)
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                buttons = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="🥀 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ🔥",
                            url=f"https://t.me/{GROUP_SUPPORT}")

                ]
            ]
        )
                await suhu.delete()
                await m.reply_photo(
                    photo=image,
                    reply_markup=buttons,
                    caption=f"**💥 {BOT_NAME}🤞Ʌɗɗɘɗ 💿 Nøω❗️\n🔊 Ʌʈ 💞 Ƥøsɩʈɩøɳ » `{pos}` 🌷 ...**",
                )
            else:
                try:
                    title = songname
                    userid = m.from_user.id
                    thumbnail = f"{IMG_5}"
                    image = await thumb(thumbnail, title, userid)
                    await suhu.edit("🔄 **Ƥɤøƈɘssɩŋʛ ...**")
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            dl,
                            HighQualityAudio(),
                        ),
                        stream_type=StreamType().local_stream,
                    )
                    add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                    await suhu.delete()
                    buttons = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="🥀 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ🔥",
                            url=f"https://t.me/{GROUP_SUPPORT}")

                ]
            ]
        )
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=image,
                        reply_markup=buttons,
                        caption=f"**💥 {BOT_NAME}🤞Mʋsɩƈ 🎸 Nøω 💞\n🔊 Ƥɭɑyɩɳʛ 😍 ØƤ 🥀 ...**",
                    )
                except Exception as e:
                    await suhu.delete()
                    await m.reply_text(f"🚫 error:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "**🤖 Wɦɑʈ 🙃 Yøʋ 💿 Wɑŋʈ 😍\n💞 Ƭø 🔊 Ƥɭɑy❓ ...**"
                )
            else:
                suhu = await c.send_message(chat_id, "🔍 **Sɘɑɤƈɦɩŋʛ ...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ **Ɲøʈɦɩŋʛ Føʋŋɗ ...**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    userid = m.from_user.id
                    image = await thumb(thumbnail, title, userid)
                    aditya, ytlink = await ytdl(url)
                    if aditya == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            buttons = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="🥀 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ🔥",
                            url=f"https://t.me/{GROUP_SUPPORT}")

                ]
            ]
        )
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=image,
                                reply_markup=buttons,
                                caption=f"**💥 {BOT_NAME}🤞Ʌɗɗɘɗ 💿 Nøω❗️\n🔊 Ʌʈ 💞 Ƥøsɩʈɩøɳ » `{pos}` 🌷 ...**",
                            )
                        else:
                            try:
                                await suhu.edit("🔄 **Ƥɤøƈɘssɩŋʛ ...**")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                        HighQualityAudio(),
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                buttons = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="🥀 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ🔥",
                            url=f"https://t.me/{GROUP_SUPPORT}")

                ]
            ]
        )
                                requester = (
                                    f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                )
                                await m.reply_photo(
                                    photo=image,
                                    reply_markup=buttons,
                                    caption=f"**💥 {BOT_NAME}🤞Mʋsɩƈ 🎸 Nøω 💞\n🔊 Ƥɭɑyɩɳʛ 😍 ØƤ 🥀 ...**",
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 error: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "**🤖 Wɦɑʈ 🙃 Yøʋ 💿 Wɑŋʈ 😍\n💞 Ƭø 🔊 Ƥɭɑy❓ ...**"
            )
        else:
            suhu = await c.send_message(chat_id, "🔍 **Sɘɑɤƈɦɩŋʛ ...**")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **Ɲøʈɦɩŋʛ Føʋŋɗ ...**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                image = await thumb(thumbnail, title, userid)
                aditya, ytlink = await ytdl(url)
                if aditya == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        buttons = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="🥀 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ🔥",
                            url=f"https://t.me/{GROUP_SUPPORT}")

                ]
            ]
        )
                        await m.reply_photo(
                            photo=image,
                            reply_markup=buttons,
                            caption=f"**💥 {BOT_NAME}🤞Ʌɗɗɘɗ 💿 Nøω❗️\n🔊 Ʌʈ 💞 Ƥøsɩʈɩøɳ » `{pos}` 🌷 ...**",
                        )
                    else:
                        try:
                            await suhu.edit("🔄 **Ƥɤøƈɘssɩŋʛ ...**")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            buttons = InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton(
                            text="🥀 ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ🔥",
                            url=f"https://t.me/{GROUP_SUPPORT}")

                ]
            ]
        )
                            await m.reply_photo(
                                photo=image,
                                reply_markup=buttons,
                                caption=f"**💥 {BOT_NAME}🤞Mʋsɩƈ 🎸 Nøω 💞\n🔊 Ƥɭɑyɩɳʛ 😍 ØƤ 🥀 ...**",
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 error: `{ep}`")
                            
