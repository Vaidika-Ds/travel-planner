import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings

async def check():
    engine = create_async_engine(settings.DATABASE_URL, connect_args={'statement_cache_size': 0})
    async with engine.connect() as conn:
        res = await conn.execute(text('SELECT id, full_name FROM user_profiles'))
        rows = res.fetchall()
        print('Users in user_profiles:', rows)
    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(check())
