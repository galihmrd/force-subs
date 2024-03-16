from pyromod import Client
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from data_json import Data


@Client.on_message(filters.group)
async def force_subs(_client, _message):
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
                        get_member = await _client.get_chat_member(
                            _message.chat.id, _message.from_user.id
                        )
                        print(get_member)
                        if get_member.status != ChatMemberStatus.ADMINISTRATOR:
                            get_channel_info = await _client.get_chat(TARGET_CHANNEL_ID)
                            await _message.reply(
                                f"""
**Hai {_message.from_user.mention}**

**Informasi:**
**Nama:** {_message.from_user.first_name} {_message.from_user.last_name}
**ID:** `{_message.from_user.id}`
**Username:** @{_message.from_user.username}

Group ini mengaktifkan fitur force subs, Kamu [harus mengikuti channel berikut]({get_channel_info.invite_link}) agar diizinkan untuk berbicara.
                                """,
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [
                                            InlineKeyboardButton(
                                                "Subscribe",
                                                url=get_channel_info.invite_link,
                                            ),
                                            InlineKeyboardButton(
                                                "Unmute",
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
                            await _message.delete()
                    except Exception as e:
                        print(e)
