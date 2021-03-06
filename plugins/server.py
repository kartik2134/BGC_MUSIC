import asyncio
import os
import sys
import math
from datetime import datetime
from time import strftime, time
import requests
import socket
import heroku3
from git import Repo
from pyrogram.types import Message
from modules.helpers.filters import command
from pyrogram import Client, filters
from os import system, execle, environ
from modules.helpers.decorators import sudo_users_only
from git.exc import InvalidGitRepositoryError
from config import UPSTREAM_REPO, BOT_USERNAME, HEROKU_API_KEY, HEROKU_APP_NAME


def gen_chlog(repo, diff):
    upstream_repo_url = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = tldr_log = ""
    ch = f"<b>updates for <a href={upstream_repo_url}/tree/{ac_br}>[{ac_br}]</a>:</b>"
    ch_tl = f"updates for {ac_br}:"
    d_form = "%d/%m/%y || %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"\n\nš¬ <b>{c.count()}</b> š <b>[{c.committed_datetime.strftime(d_form)}]</b>\n<b>"
            f"<a href={upstream_repo_url.rstrip('/')}/commit/{c}>[{c.summary}]</a></b> šØāš» <code>{c.author}</code>"
        )
        tldr_log += f"\n\nš¬ {c.count()} š [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] šØāš» {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head("main", origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)
    ac_br = repo.active_branch.name
    if "upstream" in repo.remotes:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", UPSTREAM_REPO)
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


def is_heroku():
    return "heroku" in socket.getfqdn()
    
    
@Client.on_message(filters.command(["update", f"update@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def update_repo(_, message: Message):
    chat_id = message.chat.id
    msg = await message.reply("š į“Źį“į“į“ssÉŖÉ“É¢ į“į“į“į“į“į“...")
    update_avail = updater()
    if update_avail:
        await msg.edit("ā į“į“į“į“į“į“ ŅÉŖÉ“ÉŖsŹį“į“\nā Źį“į“ Źį“sį“į“Źį“į“į“, Źį“į“į“ į“į“į“ÉŖį“ į“ į“É¢į“ÉŖÉ“ ÉŖÉ“ 1 į“ÉŖÉ“į“į“į“")
        system("git pull -f && pip3 install -r Installer")
        execle(sys.executable, sys.executable, "modules", environ)
        return
    await msg.edit("Źį“į“ ÉŖs į“į“ į“į“ į“į“į“į“ į“”ÉŖį“Ź [į“į“](https://t.me/Baddies2Buddies)", disable_web_page_preview=True)


@Client.on_message(command(["R", "/restart", "/restart@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def restart_bot(_, message: Message):
    msg = await message.reply("`Źį“sį“į“Źį“ÉŖÉ“É¢ Źį“į“...`")
    args = [sys.executable, "main.py"]
    await msg.edit("ā Źį“į“ Źį“sį“į“Źį“į“į“\nā É“į“į“” Źį“į“ į“į“É“ į“sį“ į“ŹÉŖs Źį“į“ į“É¢į“ÉŖÉ“")
    execle(sys.executable, *args, environ)
    return



@Client.on_message(filters.command(["usage", "u"]))
@sudo_users_only
async def usage_dynos(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nÉŖÉ“ į“Źį“į“Ź į“į“ į“į“į“į“į“į“ Źį“į“Ź į“į“į“, Źį“į“ É“į“į“į“ į“į“ sį“į“ į“į“ į“Źį“ `HEROKU_API_KEY` į“É“į“ `HEROKU_APP_NAME` į“ į“Źs Źį“sį“į“į“į“ÉŖį“ į“ŹŹ..."
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>į“į“į“į“ sį“Źį“ į“į“ į“į“į“ Źį“į“Ź</b> `HEROKU_API_KEY` **į“É“į“** `HEROKU_APP_NAME` <b>į“ į“Źs į“į“ŹŹį“į“į“ŹŹ ÉŖÉ“ į“Źį“į“Ź į“į“ Źį“ į“ŹŹį“ į“į“ į“į“į“į“į“į“ Źį“į“į“į“į“ŹŹ...</b>"
            )
    else:
        return await message.reply_text("į“É“ŹŹ Ņį“Ź Źį“Źį“į“į“ į“į“į“s...")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            " į“Źį“į“sį“ į“į“į“į“ sį“Źį“ Źį“į“Ź Źį“Źį“į“į“ į“į“ÉŖ į“į“Ź, Źį“į“Ź į“į“į“ É“į“į“į“ į“Źį“ į“į“É“ŅÉŖÉ¢į“Źį“į“ į“į“ŹŹį“į“į“ŹŹ ÉŖÉ“ į“Źį“ Źį“Źį“į“į“"
        )
    dyno = await message.reply_text("į“Źį“į“į“ÉŖÉ“É¢ Źį“Źį“į“į“ į“sį“É¢į“. į“Źį“į“sį“ į“”į“ÉŖį“...")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("į“É“į“ŹŹį“ į“į“ Ņį“į“į“Ź...")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
šššš ššššš


<u>į“sį“É¢į“:</u>

į“į“į“į“Ź į“sį“į“: `{AppHours}`**h**  `{AppMinutes}`**m**  [`{AppPercentage}`**%**]

<u>Źį“į“į“ÉŖÉ“ÉŖÉ“É¢ Ē«į“į“į“į“:</u>

į“į“į“į“Ź Źį“Ņį“: `{hours}`**h**  `{minutes}`**m**  [`{percentage}`**%**]"""
    return await dyno.edit(text)

