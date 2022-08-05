from aiogram import types, Router, F

import asyncio
import logging

from config import ADMIN_ID
from loader import db, bot
from cbdata import FpButtonCallbackFactory, FavMenuCallbackFactory, ReloadCallbackFactory, NotifyCallbackFactory
from keyboards import inline
from utils import me_request, broadcaster

router = Router()

# Called when user press `Add to favorites` inline button
@router.callback_query(FpButtonCallbackFactory.filter(F.cmd == "add"))
async def callback_add_to_fav(callback_query: types.CallbackQuery, callback_data: FpButtonCallbackFactory):
    symbol = callback_data.symbol
    user_id = callback_query.from_user.id
    if not await db.is_limit(user_id):
        await callback_query.answer("The limit (5) of favorite collections has been reached!", show_alert=True)
        return

    if await db.is_in_favorites(user_id, symbol):
        await callback_query.answer("Collection is already in favorites", show_alert=True)
        return

    await db.add_to_favorites(user_id, symbol, symbol.replace('_', ' ').title())
    await callback_query.answer(f"Added to favorites ({symbol})")
    await callback_query.message.edit_reply_markup(await inline.get_fav_btn(user_id, symbol))

# Called when user press `Delete from favorites` inline button
@router.callback_query(FpButtonCallbackFactory.filter(F.cmd == "del"))
async def callback_del_from_fav(callback_query: types.CallbackQuery, callback_data: FpButtonCallbackFactory):
    symbol = callback_data.symbol
    user_id = callback_query.from_user.id
    await db.delete_from_favorites(user_id, symbol)
    await callback_query.answer(f"Removed from favorites ({symbol})")
    await callback_query.message.edit_reply_markup(await inline.get_fav_btn(user_id, symbol))

# Called when user press any inline button in favmenu list
@router.callback_query(FavMenuCallbackFactory.filter(F.cmd == "fp"))
async def callback_fp(callback_query: types.CallbackQuery, callback_data: FavMenuCallbackFactory):
    symbol = callback_data.symbol
    await callback_query.message.edit_text(await me_request.format_info(await me_request.collecion_info(symbol)),
                                           reply_markup=await inline.get_favmenu_kb(symbol))
    await callback_query.answer()

# Called when user press `back` inline button in favmenu
@router.callback_query(FavMenuCallbackFactory.filter(F.cmd == "back"))
async def callback_back(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Your favorite collections:",
                                            reply_markup=await inline.get_favlist_kb(callback_query.from_user.id))
    await callback_query.answer()

# Called when user press `Delete` inline button in favmenu
@router.callback_query(FavMenuCallbackFactory.filter(F.cmd == "del"))
async def callback_back(callback_query: types.CallbackQuery, callback_data: FavMenuCallbackFactory):
    symbol = callback_data.symbol
    user_id = callback_query.from_user.id
    await db.delete_from_favorites(user_id, symbol)
    await callback_query.message.edit_text("Your favorite collections:",
                                           reply_markup=await inline.get_favlist_kb(user_id))
    await callback_query.answer(f"Removed from favorites ({symbol})")

# Called when user uses `/reload` keyboard
@router.callback_query(ReloadCallbackFactory.filter())
async def callback_reload(callback_query: types.CallbackQuery, callback_data:ReloadCallbackFactory):
    if not callback_data.approve:
        await callback_query.answer("Reload canceled")
        await callback_query.message.delete()
        return

    user_id = callback_query.from_user.id
    await db.delete_user(user_id)
    await db.add_user(user_id)
    await callback_query.answer("Your data reloaded")
    await callback_query.message.delete()

# Called when Admin uses `/notify` keyboard
@router.callback_query(NotifyCallbackFactory.filter())
async def amd_send_notify(callback_query: types.CallbackQuery, callback_data:NotifyCallbackFactory):
    if not callback_data.approve:
        await callback_query.answer("Canceled")
        await callback_query.message.delete()
        return

    users = await db.get_users()
    msg = callback_query.message.html_text
    await callback_query.message.edit_text(f"Broadcasting started, users in db: [{len(users)}] ")

    failed=[]
    succsess = 0
    try:
        for user in users:
            if await broadcaster.send_message(user, msg):
                succsess += 1
                logging.info(f"[ID:{user}]: notified successfully [{succsess}/{len(users)}]")
            else:
                failed.append(user)
            await asyncio.sleep(.05)
    finally:
        result = f"[{succsess}/{len(users)}]"
        logging.info(f"BROADCASTER: Finished finished with result {result}")

    for user_id in failed:
        await db.delete_user(user_id) 

    await bot.send_message(ADMIN_ID, f"Broadcasting finished with with result {result}\nUsers failed: {len(failed)}\n{failed}")
