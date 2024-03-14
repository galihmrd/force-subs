from pyrogram import Client, filters

from data_json import Data


@Client.on_message(filters.command("start"))
async def start(_client, _message):
    await _message.reply("Hello i'm alive!")
    Data.write_data(_message.from_user.mention, "user_id")


@Client.on_message(filters.forwarded & filters.private)
async def get_forwarded_info(_client, _message):
    await _message.reply(f"**Message Forwarded from: `{_message.forward_from_chat.id}`")


@Client.on_message(filters.command(["autoban", "fsubs"]))
async def add_channel_autoban(_client, _message):
    if _message.command[1].startswith("-"):
        data_to_write = f"{_message.command[1]}|{_message.chat.id}"
    elif _message.command[1].startswith("@"):
        try:
            get_channel_info = await _client.get_chat(_message.command[1].split("@")[1])
            data_to_write = f"{get_channel_info.id}|{_message.chat.id}"
        except Exception as e:
            return await _message.reply("**Error:**" + str(e))
    if _message.command[0] == "autoban":
        Data.write_data(data_to_write, "data_autoban_id")
    elif _message.command[0] == "fsubs":
        Data.write_data(data_to_write, "data_forcesubs_id")
    await _message.reply("Berhasil ditambahkan!")
