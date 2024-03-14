from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from data_json import Data


@Client.on_message(filters.group)
async def force_subs(_client, _message):
    if _message.text.startswith("/id"):
        await _message.reply(_message.chat.id)
    elif _message.text.startswith("/fsubs") or _message.text.startswith("/autoban"):
        command_value = _message.text.split(" ")[1]
        if command_value.startswith("-"):
            data_to_write = f"{command_value}|{_message.chat.id}"
        elif command_value.startswith("@"):
            try:
                get_channel_info = await _client.get_chat(command_value.split("@")[1])
                data_to_write = f"{get_channel_info.id}|{_message.chat.id}"
            except Exception as e:
                return await _message.reply("**Error:**" + str(e))
        elif command_value == "off":
            if _message.text.startswith("/autoban"):
                get_data_autoban = Data.get_data(_message.chat.id, "data_autoban_id")
                for data in get_data_autoban:
                    if data.endswith(str(_message.chat.id)):
                        Data.del_data(data, "data_autoban_id")
                return await _message.reply("Auto banned dimatikan!")
            elif _message.text.startswith("/fsubs"):
                get_data_autoban = Data.get_data(_message.chat.id, "data_forcesubs_id")
                for data in get_data_autoban:
                    if data.endswith(str(_message.chat.id)):
                        Data.del_data(data, "data_forcesubs_id")
                return await _message.reply("Forcesubs dimatikan!")
        if _message.text.startswith("/autoban") and command_value != "off":
            Data.write_data(data_to_write, "data_autoban_id")
        elif _message.text.startswith("/fsubs") and command_value != "off":
            Data.write_data(data_to_write, "data_forcesubs_id")
        await _message.reply("Berhasil ditambahkan!")
    else:
        user_id = _message.from_user.id
        get_data_forcesubs = Data.get_data(_message.chat.id, "data_forcesubs_id")
        for i in get_data_forcesubs:
            if i.endswith(str(_message.chat.id)):
                TARGET_CHANNEL_ID = i.split("|")[0]
                TARGET_GROUP_ID = i.split("|")[1]
        if _message.chat.id == int(TARGET_GROUP_ID):
            try:
                get_user_info = await _client.get_chat_member(
                    int(TARGET_CHANNEL_ID), user_id
                )
                if get_user_info.is_member is None:
                    status = True
                else:
                    status = False
            except UserNotParticipant:
                status = False
            if not status:
                try:
                    get_channel_info = await _client.get_chat(TARGET_CHANNEL_ID)
                    await _message.reply(
                        f"""
**Hai {_message.from_user.mention}**
**Informasi:**
    > **ID:** `{_message.from_user.id}`
    > **Username:** @{_message.from_user.username}
Group ini mengaktifkan fitur force subs, Kamu harus mengikuti channel berikut agar diizinkan untuk berbicara.
                        """,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Subscribe",
                                        url=get_channel_info.invite_link,
                                    ),
                                    InlineKeyboardButton(
                                        "Klik Disini",
                                        callback_data=f"unmute|{_message.from_user.id}|{TARGET_CHANNEL_ID}",
                                    ),
                                ],
                            ],
                        ),
                    )
                    await _client.restrict_chat_member(
                        int(TARGET_GROUP_ID),
                        user_id,
                        ChatPermissions(can_send_messages=False),
                    )
                except Exception:
                    pass
