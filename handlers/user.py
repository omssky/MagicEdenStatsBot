from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.command import CommandObject

from loader import db
from utils import me_request
from keyboards import inline
from config import __version__, START_GIF

router = Router()

# This handler will be called when user sends `/start` command
@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    if not await db.user_exists(message.from_user.id):
        await db.add_user(message.from_user.id)

    start_text = ("This bot is designed to make tracking <b>Solana NFTs</b> easier.\n"
            "Collections are searched by the collection's <b>symbol</b>*, which can be very <b>different from its name</b>."
            "So to find the collection <b>exactly</b>, enter its symbol* or use the link search!\n"
            "*can be found in the link: magiceden.io/marketplace/<u><b>SYMBOL</b></u>\n\n"
            f"Current version: {__version__} \n\n"
            "💸 Donate to the author (SOL): <code>Bqjece7hWRKnb14pEd6oUDm4NRPKe1sLSLjDbGXeX2aU</code>")
    await message.answer_video(video=START_GIF, caption=start_text, parse_mode='HTML')

# This handler will be called when user sends `/help` command
@router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    help_text = ("<b>The bot supports the following commands:</b>\n"
        "/fp <i>*collection_name*</i> - collection info by name or symbol\n"
        "/fp_link <i>*me_collecion_link*</i> - collection info by link\n"
        "/favorites - manage your favorite collection\n"
        "/reload - may help fix local bot bugs\n")
    await message.reply(help_text, parse_mode="HTML")

# This handler will be called when user sends `/fp` command
@router.message(Command(commands=["fp"]))
async def cmd_fp(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("You did not enter a name, it must be /fp <code>*collecion_name*</code>")
        return

    info_dict = await me_request.collecion_info(command.args.lower())
    if info_dict:
        await message.answer(await me_request.format_info(info_dict),
                             reply_markup=await inline.get_fav_btn(message.from_user.id, info_dict['symbol']))
        return

    await message.answer("Collection not found :(")

# This handler will be called when user sends `/fp_link` command
@router.message(Command(commands=["fp_link"]))
async def cmd_help(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("You did not enter a link, it must be\n/fp_link <code>*me_collecion_link*</code>")
        return
    collecion_link = command.args
    collection_symbol = collecion_link.lower().split('/')[-1]
    info_dict = await me_request.collecion_info(collection_symbol)
    if info_dict:
        await message.answer(await me_request.format_info(info_dict),
                             reply_markup=await inline.get_fav_btn(message.from_user.id, info_dict['symbol']))
        return

    await message.answer("Collection not found :(")

# This handler will be called when user sends `/favorites` command
@router.message(Command(commands=["favorites"]))
async def cmd_favorites(message: Message):
    keyboard = await inline.get_favlist_kb(message.from_user.id)
    if not keyboard.inline_keyboard:
        await message.answer("You have not added any collections to favorites")
        return

    await message.answer("Your favorite collections:", reply_markup=keyboard)

# This handler will be called when user sends `/reload` command
@router.message(Command(commands=["reload"]))
async def cmd_reload(message: Message):
    await message.reply(
        "⚠️This command will delete all information about your usage of the bot, this action cannot be undone, are you sure?",
        reply_markup=await inline.get_reload_kb())
