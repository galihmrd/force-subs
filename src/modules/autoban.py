from pyromod import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data_json import Data


@Client.on_chat_member_updated()
async def leaveMember(_client, _message):
    get_data_autoban = Data.get_data(_message.chat.id, "data_autoban_id")
    for i in get_data_autoban:
        if i.startswith(str(_message.chat.id)):
            TARGET_CHANNEL_ID = i.split("|")[0]
            TARGET_GROUP_ID = i.split("|")[1]
    try:
        if int(TARGET_CHANNEL_ID) == _message.chat.id:
            try:
                bot_id = await _client.get_me()
                if _message.old_chat_member.restricted_by.id == bot_id.id:
                    return False
            except AttributeError:
                try:
                    await _client.send_message(
                        int(TARGET_GROUP_ID),
                        f"""
**#AUTOBAN**
{_message.old_chat_member.user.mention} (`{_message.old_chat_member.user.id}`) diblokir karena meninggalkan channel
klik tombol dibawah ini untuk membuka blokir.
                        """,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "Buka Blokir",
                                        callback_data=f"unblock|{_message.from_user.id}|{TARGET_CHANNEL_ID}",
                                    ),
                                ],
                            ],
                        ),
                    )
                    await _client.ban_chat_member(
                        int(TARGET_CHANNEL_ID), _message.from_user.id
                    )
                except AttributeError:
                    pass
    except UnboundLocalError:
        pass
