from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from cbdata import FpButtonCallbackFactory, FavMenuCallbackFactory, ReloadCallbackFactory, NotifyCallbackFactory
from loader import db

#  This function returns add/delete button, based on the data from the database
async def get_fav_btn(user_id, collection_symbol) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    if await db.is_in_favorites(user_id, collection_symbol):
        keyboard.button(text="Delete from favorites 🚫", callback_data=FpButtonCallbackFactory(cmd="del", symbol=collection_symbol))
    else:
        keyboard.button(text="Add to favorites ⭐️", callback_data=FpButtonCallbackFactory(cmd="add", symbol=collection_symbol))
    return keyboard.as_markup()

# This function returns the delete and back buttons in one row (used in favmenu)
async def get_favmenu_kb(collection_symbol) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text = "↩️", callback_data=FavMenuCallbackFactory(cmd="back", symbol='').pack()),
            InlineKeyboardButton(text="Delete 🚫", callback_data=FavMenuCallbackFactory(cmd="del", symbol=collection_symbol).pack())
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# This function returns keyboard with user favorite collections, based on the data from the database
async def get_favlist_kb(user_id) -> InlineKeyboardMarkup:
    favlist = await db.get_user_favorites(user_id)
    keyboard = InlineKeyboardBuilder()
    for collecion in favlist:
        keyboard.button(text=collecion[1], callback_data=FavMenuCallbackFactory(cmd="fp", symbol=collecion[0]))
    keyboard.adjust(1)
    return keyboard.as_markup()

# This function returns the Yes and buttons in one row (used in reload)
async def get_reload_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Yes ✅", callback_data=ReloadCallbackFactory(approve=True).pack()),
            InlineKeyboardButton(text="No 🚫", callback_data=ReloadCallbackFactory(approve=False).pack())
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

# This function returns the Yes and buttons in one row (used in reload)
async def get_notify_kb() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Send ✉️", callback_data=NotifyCallbackFactory(approve=True).pack()),
            InlineKeyboardButton(text="Cancel 🚫", callback_data=NotifyCallbackFactory(approve=False).pack())
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard