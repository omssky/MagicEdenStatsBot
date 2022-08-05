from aiogram.dispatcher.filters.callback_data import CallbackData

class FpButtonCallbackFactory(CallbackData, prefix="fp"):   #fp:cmd:symbol
    cmd: str
    symbol: str

class FavMenuCallbackFactory(CallbackData, prefix="fm"):    #fm:cmd:symbol
    cmd: str
    symbol: str

class ReloadCallbackFactory(CallbackData, prefix="reload"): #reload:approve
    approve: bool

class NotifyCallbackFactory(CallbackData, prefix="notify"): #reload:approve
    approve: bool
