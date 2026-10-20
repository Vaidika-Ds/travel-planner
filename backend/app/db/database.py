from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# In case DATABASE_URL is not set yet in .env, fallback to SQLite in memory to prevent crash
db_url = settings.DATABASE_URL
if not db_url:
    # default fallback or placeholder
    db_url = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    db_url,
    echo=(settings.ENVIRONMENT == "development"),
    future=True,
    connect_args={"statement_cache_size": 0}  # Required for Supabase Transaction Pooler
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    """Dependency for providing an async database session per request"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
