import aiosqlite
from config.config import DB_PATH


async def create_user(id_tg: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("INSERT INTO users (id_tg) VALUES (?)", (id_tg,))
        await conn.commit()
    return True


async def get_user(id_tg: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE id_tg = ?", (id_tg,))
        return await cursor.fetchone()

async def get_users():
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cursor = await conn.execute("SELECT * FROM users")
        users = await cursor.fetchall()
        return [dict(u) for u in users]
        

async def update_user(id_tg: int, **kwargs):
    async with aiosqlite.connect(DB_PATH) as conn:
        for parameter, value in kwargs.items():
            await conn.execute(
                f"UPDATE users SET {parameter} = ? WHERE id_tg = ?", (value, id_tg)
            )
        await conn.commit()
    return True


async def delete_user(id_tg: int):
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("DELETE FROM users WHERE id_tg = ?", (id_tg,))
        await conn.commit()
    return True
