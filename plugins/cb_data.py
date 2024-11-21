from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db

from PIL import Image
import os
import time

import humanize



# Born to make history @LazyDeveloper !
@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    user_id = update.message.chat.id
    date = update.message.date
    await update.message.delete()
    await update.message.reply_text("__𝙿𝚕𝚎𝚊𝚜𝚎 𝙴𝚗𝚝𝚎𝚛 𝙽𝚎𝚠 𝙵𝚒𝚕𝚎𝙽𝚊𝚖𝚎...__",
                                    reply_to_message_id=update.message.reply_to_message.id,
                                    reply_markup=ForceReply(True))

@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    type = update.data.split("_")[1]
    user_id = int(update.message.chat.id)
    new_name = update.message.text
    new_filename = new_name.split(":-")[1]
    file_path = f"downloads/{user_id}{time.time()}/{new_filename}"
    file = update.message.reply_to_message
    ms = await update.message.edit("⚠️__Please wait...__\n__Downloading file to my server...__")
    c_time = time.time()
    # try:
    #     path = await bot.download_media(message=file, progress=progress_for_pyrogram, progress_args=(f"\nDownload in progress...\n\n{new_filename}",  ms, c_time))
    # except Exception as e:
    #     await ms.edit(e)
    #     return

    try:
        path = await file.download(file_name=file_path, progress=progress_for_pyrogram, progress_args=(f"Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....\n\n{new_filename}", ms, c_time))
    except Exception as e:
        return await ms.edit(e)
    duration = 0
    # 

    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    except:
        pass


    # splitpath = path.split("/downloads/")
    # dow_file_name = splitpath[1]
    # old_file_name = f"downloads/{dow_file_name}"
    # os.rename(old_file_name, file_path)
    # duration = 0
    
    
    # try:
    #     metadata = extractMetadata(createParser(file_path))
    #     if metadata.has("duration"):
    #         duration = metadata.get('duration').seconds
    # except:
    #     pass


    ph_path = None
    media = getattr(file, file.media.value)
    c_caption = await db.get_caption(update.message.chat.id)
    c_thumb = await db.get_thumbnail(update.message.chat.id)
    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanize.naturalsize(
                media.file_size), duration=convert(duration))
        except Exception as e:
            await ms.edit(text=f"Your caption Error unexpected keyword ●> ({e})")
            return
    else:
        caption = f"{new_filename}"
    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await bot.download_media(c_thumb)
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
    await ms.edit("⚠️__Please wait...__\n__Processing file upload....__")
    c_time = time.time()
    try:
        if type == "document":
            await bot.send_document(
                update.message.chat.id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("⚠️__Please wait...__\n__Processing file upload....__",  ms, c_time))
        elif type == "video":
            await bot.send_video(
                update.message.chat.id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("⚠️__Please wait...__\n__Processing file upload....__",  ms, c_time))
        elif type == "audio":
            await bot.send_audio(
                update.message.chat.id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("⚠️__Please wait...__\n__Processing file upload....__",  ms, c_time))
    except Exception as e:
        await ms.edit(f" Erro {e}")
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        return
    await ms.delete()
    os.remove(file_path)
    if ph_path:
        os.remove(ph_path)



# @Client.on_callback_query(filters.regex("upload"))
# async def rename_callback(bot, query):
#     user_id = query.from_user.id
#     file_name = query.message.text.split(":-")[1]
#     file_path = f"downloads/{user_id}{time.time()}/{file_name}"
#     file = query.message.reply_to_message

#     sts = await query.message.edit("Tʀyɪɴɢ Tᴏ Dᴏᴡɴʟᴏᴀᴅɪɴɢ....")
#     try:
#         path = await file.download(file_name=file_path, progress=progress_for_pyrogram, progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time()))
#     except Exception as e:
#         return await sts.edit(e)
#     duration = 0
#     try:
#         metadata = extractMetadata(createParser(file_path))
#         if metadata.has("duration"):
#             duration = metadata.get('duration').seconds
#     except:
#         pass

#     ph_path = None
#     media = getattr(file, file.media.value)
#     db_caption = await db.get_caption(user_id)
#     db_thumb = await db.get_thumbnail(user_id)

#     if db_caption:
#         try:
#             caption = db_caption.format(filename=file_name, filesize=humanbytes(
#                 media.file_size), duration=convert(duration))
#         except KeyError:
#             caption = f"**{file_name}**"
#     else:
#         caption = f"**{file_name}**"

#     if (media.thumbs or db_thumb):
#         if db_thumb:
#             ph_path = await bot.download_media(db_thumb)
#         else:
#             ph_path = await bot.download_media(media.thumbs[0].file_id)
#         Image.open(ph_path).convert("RGB").save(ph_path)
#         img = Image.open(ph_path)
#         img.resize((320, 320))
#         img.save(ph_path, "JPEG")

#     await sts.edit("Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....")
#     type = query.data.split("_")[1]
#     try:
#         if type == "document":
#             await sts.reply_document(
#                 document=file_path,
#                 thumb=ph_path,
#                 caption=caption,
#                 progress=progress_for_pyrogram,
#                 progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
#             )
#         elif type == "video":
#             await sts.reply_video(
#                 video=file_path,
#                 caption=caption,
#                 thumb=ph_path,
#                 duration=duration,
#                 progress=progress_for_pyrogram,
#                 progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
#             )
#         elif type == "audio":
#             await sts.reply_audio(
#                 audio=file_path,
#                 caption=caption,
#                 thumb=ph_path,
#                 duration=duration,
#                 progress=progress_for_pyrogram,
#                 progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
#             )
#     except Exception as e:
#         try:
#             os.remove(file_path)
#             os.remove(ph_path)
#             return await sts.edit(f" Eʀʀᴏʀ {e}")
#         except:
#             pass

#     try:
#         os.remove(file_path)
#         os.remove(ph_path)
#         await sts.delete()
#     except:
#         pass
