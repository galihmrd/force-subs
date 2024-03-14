from pyrogram import Client, filters


@Client.on_callback_query(filters.regex(pattern=r"unblock"))
async def ublock(b, cb):
    if cb.from_user.id in SUDO:
        user_id = int(cb.data.strip().split("|")[1])
        await b.unban_chat_member(int(TARGET_CHANNEL_ID), user_id)
        await cb.message.edit(f"{user_id} Dihapus dari daftar blokir")
    else:
        await cb.answer("Anda tidak memiliki izin!", show_alert=True)
