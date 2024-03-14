from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import ChatPermissions


@Client.on_callback_query(filters.regex(pattern=r"unblock"))
async def ublock(b, cb):
    user_id = int(cb.data.strip().split("|")[1])
    TARGET_CHANNEL_ID = int(cb.data.strip().split("|")[2])
    get_user_info = await b.get_chat_member(TARGET_CHANNEL_ID, cb.from_user.id)
    try:
        if get_user_info.privileges.can_restrict_members:
            await b.unban_chat_member(int(TARGET_CHANNEL_ID), user_id)
            await cb.message.edit(f"{user_id} Dihapus dari daftar blokir")
        else:
            await cb.answer(
                "Anda kekurangan izin: can_restrict_members", show_alert=True
            )
    except UserNotParticipant:
        await cb.answer("Anda harus menjadi admin untuk melakukan ini!", show_alert=True)
    except AttributeError:
        await cb.answer("Anda harus menjadi admin untuk melakukan ini!", show_alert=True)


@Client.on_callback_query(filters.regex(pattern=r"unmute"))
async def unmute(b, cb):
    user_id = int(cb.data.strip().split("|")[1])
    TARGET_CHANNEL_ID = int(cb.data.strip().split("|")[2])
    try:
        get_user_info = await b.get_chat_member(TARGET_CHANNEL_ID, user_id)
        if get_user_info.is_member is None:
            status = True
        else:
            status = False
    except UserNotParticipant:
        status = False
    if status:
        try:
            await b.restrict_chat_member(
                cb.message.chat.id,
                user_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                ),
            )
            await cb.message.delete()
        except Exception as e:
            await cb.answer("Errror: " + str(e))
    else:
        await cb.answer(
            "Anda belum bergabung/subscribe channel tertaut!", show_alert=True
        )
