from aiogram import Router, types
from aiogram.dispatcher.filters import ContentTypesFilter

router = Router()

# This handler will be called when user sends any unknown command/message
@router.message(ContentTypesFilter(content_types=[types.ContentType.ANY]))
async def unknown_message(message: types.Message):
    await message.reply("Unknown command, go to /help")
    