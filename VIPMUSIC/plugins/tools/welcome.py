import os
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from VIPMUSIC import LOGGER
from pyrogram.types import Message
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC import app
from VIPMUSIC.utils.database import *

LOGGER = getLogger(__name__)


class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chat, id, uname):
    background = Image.open("assets/wel2.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize(
        (500, 500)
    ) 
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('assets/font.ttf', size=60)
    font2 = ImageFont.truetype('assets/font.ttf', size=90)
    
    saffron = (255, 153, 51)  
    white = (255, 255, 255)   
    green = (19, 136, 8)
    
    draw.text((650, 250), f'NAME : {unidecode(user)}', fill="white", font=font)
    draw.text((650, 350), f'ID : {id}', fill="white", font=font)
    draw.text((650, 450), f"USERNAME : {uname}", fill="white",font=font)
    pfp_position = (100, 133)  
    background.paste(pfp, pfp_position, pfp)  
    background.save(
        f"downloads/welcome#{id}.png"
    )
    return f"downloads/welcome#{id}.png"


@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = "**â– á´œsá´€É¢á´‡ âž¥** /swel [á´‡É´á´€Ê™ÊŸá´‡|á´…Éªsá´€Ê™ÊŸá´‡]"
    if len(message.command) == 1:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
      A = await wlcm.find_one({"chat_id" : chat_id})
      state = message.text.split(None, 1)[1].strip()
      state = state.lower()
      if state == "enable":
        if A:
           return await message.reply_text("âœ¦ Special Welcome Already Enabled")
        elif not A:
           await add_wlcm(chat_id)
           await message.reply_text(f"âœ¦ Enabled Special Welcome in {message.chat.title}")
      elif state == "disable":
        if not A:
           return await message.reply_text("âœ¦ Special Welcome Already Disabled")
        elif A:
           await rm_wlcm(chat_id)
           await message.reply_text(f"âœ¦ Disabled Special Welcome in {message.chat.title}")
      else:
        await message.reply_text(usage)
    else:
        await message.reply("âœ¦ Only Admins Can Use This Command")
 
@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
   # A = await wlcm.find_one({"chat_id" : chat_id})
   # if not A:
  #     return
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"pp{user.id}.png"
        )
    except AttributeError:
        pic = "assets/upic.png"
    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption= f"""
 â€¢â—â—‰âœ¿ á´¡á´‡ÊŸá´„á´á´á´‡ Ê™á´€Ê™Ê âœ¿â—‰â—â€¢
â–°â–±â–±â–±â–±â–±â–±â–±â–±â–±â–±â–±â–±â–±â–°

â˜‰ É´á´€á´á´‡ âž¥  {user.mention}
â˜‰ á´œsá´‡Ê€É´á´€á´á´‡ âž¥  @{user.username}
â˜‰ á´œsá´‡Ê€ Éªá´… âž¥  {user.id}
â˜‰ ð“á´á´›á´€ÊŸ ðŒá´‡á´Ê™á´‡Ê€s â§½ {count}**
â˜‰ á´˜á´á´¡á´‡Ê€á´‡á´… Ê™Ê âž¥ à¹›[â¤ï¸â€ðŸ”¥ â€¢ ð›šð›ð›š â€¢ â¤ï¸â€ðŸ”¥ ](https://t.me/ll_SARKAR_MERA_BABU_ll)
â–°â–±â–±â–±â–±â–±â–±â–±â–±â–±â–±â–±â–±â–±â–°
""",
reply_markup=InlineKeyboardMarkup(
[InlineKeyboardButton(f"❍ 𓆩 𝗦𝐓𝐘𝐋𝐈𝐒𝐇 ⌯ 𝗡𝐀𝐌𝐄 𓆪 ❍", url=f"https://t.me/TG_NAME_STYLE"),
[InlineKeyboardButton(f"❍ 𝐏𝐑𝐎𝐌𝐎𝐓𝐈𝐎𝐍 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 ❍", url=f"https://t.me/TG_NAME_STYLE/4602"),
]
]
))

    except Exception as e:
        LOGGER.error(e)
    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception as e:
        pass


      
