from pyrogram import Client, filters

from data_json import Data
from config import SUDO_USERS


@Client.on_message(filters.command("start"))
async def start(_client, _message):
    await _message.reply("Hello i'm alive!")
    Data.write_data(_message.from_user.mention, "user_id")


@Client.on_message(filters.forwarded & filters.private)
async def get_forwarded_info(_client, _message):
    await _message.reply(f"**Message Forwarded from: `{_message.forward_from_chat.id}`")


@Client.on_message(filters.command(["auth", "unauth"]))
async def authorize(_client, _message):
    list_sudo = SUDO_USERS.split(" ")
    command_value = _message.command[1]
    if str(_message.from_user.id) in list_sudo:
        if _message.command[1].startswith("@"):
            get_user_info = await _client.get_chat(command_value.split("@")[1])
            user_id = get_user_info.id
        elif _message.command[1].startswith("-"):
            user_id = message.command[1]
        else:
            return await _message.reply("Invalid input!")
        if _message.command[0] == "auth":
            Data.write_data(str(user_id), "authorized_user_id")
            return await _message.reply("Akses berhasil diberikan!")
        elif _message.command[0] == "unauth":
            Data.del_data(str(user_id), "authorized_user_id")
            return await _message.reply("Akses berhasil dihapus!")
    else:
        return await _message.reply("Anda tidak memiliki izin!")
