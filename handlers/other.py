from distutils.command.config import config
from aiogram import Router, types, F
from aiogram.dispatcher.filters import ContentTypesFilter
import config

router = Router()

# This handler will be called when user sends any unknown command/message
@router.message(ContentTypesFilter(content_types=[types.ContentType.ANY]))
async def unknown_message(message: types.Message):
    print(message)
    res = F.chat.id == config.ADMIN_ID
    print(res)
    await message.reply("Unknown command, go to /help")