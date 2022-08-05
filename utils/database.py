from array import array
import logging
import aiosqlite

class DataBase:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
    
    async def create_db(self) -> None:
        async with aiosqlite.connect(self.db_path) as connection:
            await connection.execute("CREATE TABLE IF NOT EXISTS users(_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL)")
            await connection.execute("CREATE TABLE IF NOT EXISTS favorites(_id INTEGER PRIMARY KEY AUTOINCREMENT, key_user INTEGER NOT NULL, col_symbol TEXT, col_name TEXT, FOREIGN KEY(key_user) REFERENCES users(id))")
            await connection.commit()

    async def user_exists(self, user_id) -> bool:
            async with aiosqlite.connect(self.db_path) as connection:
                async with connection.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)) as cursor:
                    return bool(await cursor.fetchone())

    async def add_user(self, user_id) -> None:
        async with aiosqlite.connect(self.db_path) as connection:
            await connection.execute("INSERT INTO users(user_id) VALUES (?)", (user_id,))
            await connection.commit()
            logging.info(f"[ID:{user_id}]: added TO DB")

    async def delete_user(self, user_id) -> None:
        async with aiosqlite.connect(self.db_path) as connection:
            await connection.execute("DELETE FROM favorites WHERE key_user = (SELECT _id FROM users WHERE user_id = ?)", (user_id,))
            await connection.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            await connection.commit()
            logging.info(f"[ID:{user_id}]: deleted from DB")
    
    async def get_users(self) -> array:
        async with aiosqlite.connect(self.db_path) as connection:
            async with connection.execute("SELECT user_id FROM users") as cursor:
                users = await cursor.fetchall()
                return [user[0] for user in users]

    async def get_users_count(self) -> int:
            async with aiosqlite.connect(self.db_path) as connection:
                async with connection.execute("SELECT COUNT(_id) FROM users") as cursor:
                    user_ids = await cursor.fetchone()
                    return user_ids[0]

    async def is_in_favorites(self, user_id, collection_symbol) -> bool:
            async with aiosqlite.connect(self.db_path) as connection:
                async with connection.execute("SELECT * FROM favorites JOIN users ON favorites.key_user = users._id WHERE user_id = ? AND col_symbol = ?", (user_id, collection_symbol)) as cursor:
                    return bool(await cursor.fetchone())
    
    async def is_limit(self, user_id) -> bool:
        async with aiosqlite.connect(self.db_path) as connection:
                async with connection.execute("SELECT COUNT(*) FROM favorites JOIN users ON favorites.key_user = users._id WHERE user_id = ?", (user_id,)) as cursor:
                    count = await cursor.fetchone()
                    return count[0] < 5

    async def add_to_favorites(self, user_id, collection_symbol, collection_name) -> None:
        async with aiosqlite.connect(self.db_path) as connection:
            await connection.execute("INSERT INTO favorites(key_user, col_symbol, col_name) VALUES ((SELECT _id FROM users WHERE user_id = ?), ?, ?)", (user_id, collection_symbol, collection_name))
            await connection.commit()

    async def delete_from_favorites(self, user_id, collection_symbol) -> None:
        async with aiosqlite.connect(self.db_path) as connection:
            await connection.execute("DELETE FROM favorites WHERE key_user = (SELECT _id FROM users WHERE user_id = ?) AND col_symbol = ?", (user_id, collection_symbol))
            await connection.commit()

    async def get_user_favorites(self, user_id) -> array:
            async with aiosqlite.connect(self.db_path) as connection:
                async with connection.execute("SELECT col_symbol, col_name FROM favorites JOIN users ON favorites.key_user = users._id WHERE user_id = ?", (user_id,)) as cursor:
                    return await cursor.fetchall()

    async def get_collections_count(self) -> int:
        async with aiosqlite.connect(self.db_path) as connection:
                async with connection.execute("SELECT COUNT(_id) FROM favorites") as cursor:
                    count = await cursor.fetchone()
                    return count[0]
    