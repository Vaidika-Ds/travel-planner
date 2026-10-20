import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')

async def test_db():
    from app.core.config import settings
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy import text

    print("Testing database connection...")
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name"))
            rows = result.fetchall()
            print("Connection SUCCESSFUL!")
            print(f"Found {len(rows)} tables in Supabase:")
            for row in rows:
                print(f"  - {row[0]}")
    except Exception as e:
        print(f"Connection FAILED: {e}")
    finally:
        await engine.dispose()

asyncio.run(test_db())
