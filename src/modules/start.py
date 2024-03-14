from pyrogram import Client, filters

from data_json import Data


@Client.on_message(filters.command("start"))
async def start(_client, _message):
    await _message.reply("Hello i'm alive!")
    Data.write_data(_message.from_user.mention, "user_id")


@Client.on_message(filters.forwarded)
async def get_forwarded_info(_client, _message):
    await _message.reply(f"**Message Forwarded from: `{_message.forward_from_chat.id}`")


@Client.on_message(filters.command("add"))
async def add_channel_autoban(_client, _message):
    Data.write_data(_message.command[1], "data_autoban_id")
    await _message.reply("Berhasil ditambahkan!")

@Client.on_message(filters.command("fsubs"))
async def add_channel_forcesubs(_client, _message):
    Data.write_data(_message.command[1], "data_forcesubs_id")
    await _message.reply("Berhasil ditambahkan!")
