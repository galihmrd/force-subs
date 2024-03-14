from pyrogram import Client, filters


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
            await cb.answer("Anda kekurangan izin: can_restrict_members", show_alert=True)
    except AttributeError:
        await cb.answer("Anda harus jadi admin untuk melakukan ini!", show_alert=True)
