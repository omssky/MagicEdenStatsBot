from environs import Env

env = Env()

TOKEN = env.str("TOKEN")
ADMIN_ID = env.int("ADMIN_ID")
__version__ = env.str("VERSION")
START_GIF = env.str("START_GIF")
