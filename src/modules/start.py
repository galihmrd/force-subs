from pyrogram import Client, filters

from config import SUDO_USERS
from data_json import Data


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
            user_id = _message.command[1]
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


@Client.on_message(filters.command(["autoban", "fsubs"]))
async def controler(_client, _message):
    command_value = " ".join(_message.command[1:])
    if command_value.startswith("-"):
        data_to_write = command_value
        if _message.command[0] == "autoban" and "off" not in command_value:
            Data.write_data(data_to_write, "data_autoban_id")
        elif _message.command[0] == "fsubs" and not "off" in command_value:
            Data.write_data(data_to_write, "data_forcesubs_id")
        return await _message.reply("Berhasil ditambahkan!")
    elif "off" in command_value:
        if _message.command[0] == "autoban":
            get_data_autoban = Data.get_data(
                command_value.split("off_")[1], "data_autoban_id"
            )
            for data in get_data_autoban:
                if data.endswith(command_value.split("off_")[1].split("|")[1]):
                    Data.del_data(data, "data_autoban_id")
            return await _message.reply("Auto banned dimatikan!")
        elif _message.command[0] == "fsubs":
            get_data_autoban = Data.get_data(
                command_value.split("off_")[1], "data_forcesubs_id"
            )
            print(command_value.split("off_")[1].split("|")[1])
            for data in get_data_autoban:
                if data.endswith(command_value.split("off_")[1].split("|")[1]):
                    Data.del_data(data, "data_forcesubs_id")
                return await _message.reply("Forcesubs dimatikan!")
