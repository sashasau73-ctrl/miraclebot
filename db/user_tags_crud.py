import aiosqlite
from config.config import DB_PATH, TAGS



async def crate_user_tag(user_id: int, tag_name: str):
    if tag_name not in TAGS:
        async with aiosqlite.connect(DB_PATH) as conn:
            await conn.execute("SELECT id FROM tags WHERE name = ?", (tag_name,))
            tag_id = await conn.fetchone()
            await conn.execute(
                "INSERT INTO users_tags (user_id, tag_id) VALUES (?, ?)",
                (user_id, tag_id[0]),
                )
            await conn.commit()
            return True
    return False    