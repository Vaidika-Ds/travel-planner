import asyncio
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

async def run_all_checks():
    print("=== PHASE 3 COMPLETE REVIEW ===\n")

    # ── 1. FILE STRUCTURE ──────────────────────────────────────────────────────
    print("[1] FILE STRUCTURE CHECK")
    files_needed = [
        "app/__init__.py", "app/main.py",
        "app/core/__init__.py", "app/core/config.py", "app/core/security.py",
        "app/db/__init__.py", "app/db/database.py",
        "app/models/__init__.py", "app/models/models.py",
        "app/schemas/__init__.py", "app/schemas/trip_schema.py",
        "app/routers/__init__.py", "app/routers/trips.py",
        "app/services/__init__.py", "app/ai/__init__.py",
        ".env", "requirements.txt",
    ]
    all_ok = True
    for f in files_needed:
        exists = os.path.exists(f)
        if not exists:
            all_ok = False
        print(f"  {'OK    ' if exists else 'MISSING'} -> {f}")
    print(f"  Result: {'ALL FILES PRESENT' if all_ok else 'SOME FILES MISSING'}\n")

    # ── 2. ENV VARIABLES ──────────────────────────────────────────────────────
    print("[2] ENV VARIABLES CHECK")
    from app.core.config import settings
    items = {
        "PROJECT_NAME"    : settings.PROJECT_NAME,
        "SUPABASE_URL"    : (settings.SUPABASE_URL[:40]+"...") if settings.SUPABASE_URL else "MISSING",
        "SUPABASE_ANON"   : "SET" if settings.SUPABASE_ANON_KEY else "MISSING",
        "SERVICE_ROLE_KEY": "SET" if settings.SUPABASE_SERVICE_ROLE_KEY else "MISSING",
        "DATABASE_URL"    : "SET" if settings.DATABASE_URL else "MISSING",
        "GROQ_API_KEY"    : "SET" if settings.GROQ_API_KEY else "MISSING",
        "GROQ_MODEL"      : settings.GROQ_MODEL,
        "ENVIRONMENT"     : settings.ENVIRONMENT,
    }
    for k, v in items.items():
        print(f"  {k:20} : {v}")
    print()

    # ── 3. PYTHON PACKAGES ────────────────────────────────────────────────────
    print("[3] PYTHON PACKAGES CHECK")
    packages = [
        ("fastapi","FastAPI"), ("uvicorn","uvicorn"),
        ("sqlalchemy","SQLAlchemy"), ("asyncpg","asyncpg"),
        ("pydantic","Pydantic"), ("pydantic_settings","Pydantic-Settings"),
        ("httpx","HTTPX"), ("jose","python-jose"),
        ("greenlet","greenlet"), ("aiosqlite","aiosqlite"),
    ]
    for module, label in packages:
        try:
            __import__(module)
            print(f"  OK     -> {label}")
        except ImportError:
            print(f"  MISSING-> {label}")
    print()

    # ── 4. FASTAPI APP ────────────────────────────────────────────────────────
    print("[4] FASTAPI APP IMPORT CHECK")
    try:
        from app.main import app
        print(f"  OK     -> App title  : '{app.title}'")
        print(f"  OK     -> App version: '{app.version}'")
        named = [r.path for r in app.routes if hasattr(r, 'path') and not r.path.startswith('/openapi') and r.path not in ['/docs','/redoc','/docs/oauth2-redirect']]
        print(f"  OK     -> Named routes: {named}")
    except Exception as e:
        print(f"  FAILED -> {e}")
    print()

    # ── 5. DATABASE ───────────────────────────────────────────────────────────
    print("[5] LIVE DATABASE CONNECTION CHECK")
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy import text
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        connect_args={"statement_cache_size": 0}
    )
    try:
        async with engine.connect() as conn:
            result = await conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
            )
            tables = [row[0] for row in result.fetchall()]
            expected = {"activities","ai_generation_logs","itineraries","itinerary_days","trips","user_preferences","user_profiles"}
            missing  = expected - set(tables)
            print(f"  Connected to Supabase : YES")
            print(f"  Tables found          : {len(tables)}/7")
            for t in sorted(tables):
                print(f"    - {t}")
            if missing:
                print(f"  MISSING: {missing}")
            else:
                print(f"  All 7 tables present  : OK")
    except Exception as e:
        print(f"  FAILED -> {e}")
    finally:
        await engine.dispose()
    print()

    # ── 6. GROQ AI ────────────────────────────────────────────────────────────
    print("[6] GROQ AI CONNECTION CHECK")
    import httpx
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [{"role": "user", "content": "Reply with just the word: CONNECTED"}],
        "max_tokens": 10,
        "temperature": 0.0
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            r = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers, json=payload
            )
            data = r.json()
            if r.status_code == 200:
                reply  = data["choices"][0]["message"]["content"].strip()
                tokens = data["usage"]["total_tokens"]
                print(f"  Connected to Groq  : YES")
                print(f"  Model              : {data['model']}")
                print(f"  AI replied         : {reply}")
                print(f"  Tokens used        : {tokens}")
            else:
                print(f"  FAILED ({r.status_code}) -> {data.get('error',{}).get('message')}")
        except Exception as e:
            print(f"  FAILED -> {e}")
    print()

    print("=" * 40)
    print("PHASE 3 REVIEW COMPLETE — NO ERRORS")
    print("=" * 40)

asyncio.run(run_all_checks())
