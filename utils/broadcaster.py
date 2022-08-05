from aiogram import exceptions
from asyncio import sleep
import logging

from loader import bot

# Safe message sender to use in broadcasting
async def send_message(user_id: int, text: str) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=True, disable_web_page_preview=True)
    except exceptions.TelegramForbiddenError as err:
        logging.error(f"[ID:{user_id}]: {err.message}")
    except exceptions.TelegramNotFound as err:
        logging.error(f"[ID:{user_id}]: {err.message}")
    except exceptions.TelegramRetryAfter as err:
        logging.error(f"[ID:{user_id}]: Flood limit is exceeded. Sleep {err.retry_after} seconds.")
        await sleep(err.retry_after)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.TelegramBadRequest as err:
        logging.error(f"[ID:{user_id}]: {err.message}")
    except exceptions.TelegramAPIError as err:
        logging.exception(f"[ID:{user_id}]: {err.message}")
    else:
        return True
    return False
    