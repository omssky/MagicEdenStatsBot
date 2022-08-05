from aiogram import Router, F
from aiogram.types import Message
import aiogram.utils.markdown as fmt
from aiogram.dispatcher.filters.command import Command

from loader import bot, db
from keyboards import inline
from config import ADMIN_ID, __version__

router = Router()
router.message.filter(F.chat.id == ADMIN_ID)

# Called when ADMIN sends `/stats` command
@router.message(Command(commands=["stats"]))
async def adm_stats(message: Message):
    reply_text = fmt.text(
                fmt.text("Vesrion:", __version__),
                fmt.text("Users count:", await db.get_users_count()),
                fmt.text("Collecions count:", await db.get_collections_count()),
                sep="\n")
    await message.answer(reply_text)

# Called when ADMIN sends `/notify` command
@router.message_handler(Command(commands=["notify"]))
async def adm_notify(message: Message):
    msg = message.html_text
    await message.reply(text=msg.replace("/notify", ''), reply_markup=await inline.get_notify_kb())
    