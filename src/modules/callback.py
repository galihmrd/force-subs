from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import ChatPermissions


@Client.on_callback_query(filters.regex(pattern=r"unblock"))
async def ublock(b, cb):
    user_id = int(cb.data.strip().split("|")[1])
    TARGET_CHANNEL_ID = int(cb.data.strip().split("|")[2])
    try:
        get_user_info = await b.get_chat_member(TARGET_CHANNEL_ID, cb.from_user.id)
        if get_user_info.privileges.can_restrict_members:
            await b.unban_chat_member(int(TARGET_CHANNEL_ID), user_id)
            await cb.message.edit(f"{user_id} Dihapus dari daftar blokir")
        else:
            await cb.answer(
                "Anda kekurangan izin: can_restrict_members", show_alert=True
            )
    except UserNotParticipant:
        await cb.answer(
            "Anda harus menjadi admin untuk melakukan ini!", show_alert=True
        )
    except AttributeError:
        await cb.answer(
            "Anda harus menjadi admin untuk melakukan ini!", show_alert=True
        )


@Client.on_callback_query(filters.regex(pattern=r"unmute"))
async def unmute(b, cb):
    user_id = int(cb.data.strip().split("|")[1])
    TARGET_CHANNEL_ID = int(cb.data.strip().split("|")[2])
    if cb.from_user.id != int(user_id):
        return await cb.answer("Tugas ini bukan untuk anda!", show_alert=True)
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
            get_user_info = await b.get_users(user_id)
            await b.restrict_chat_member(
                cb.message.chat.id,
                user_id,
                ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                ),
            )
            await cb.message.edit(f"__{get_user_info.mention} Kini dapat berbicara!__")
        except Exception as e:
            await cb.answer("Errror: " + str(e))
    else:
        await cb.answer("Subscribe channel tertaut terlebih dahulu!", show_alert=True)
