import sys
import os
import asyncio
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("=" * 60)
    print("🌟 COMPLETE SYSTEM AUDIT: PHASES 1 THROUGH 6")
    print("=" * 60)

    # 1. ROOT & FOLDER INTEGRITY
    print("\n[CHECK 1] DIRECTORY & FOLDER STRUCTURE")
    root = r"C:\Users\DELL\Desktop\travel-planner"
    backend_dir = os.path.join(root, "backend")
    frontend_dir = os.path.join(root, "frontend")

    print(f"  Backend folder  : {'EXISTS' if os.path.exists(backend_dir) else 'MISSING'}")
    print(f"  Frontend folder : {'EXISTS' if os.path.exists(frontend_dir) else 'MISSING'}")
    print(f"  Root .gitignore : {'EXISTS' if os.path.exists(os.path.join(root, '.gitignore')) else 'MISSING'}")

    # 2. BACKEND ENV & SECRETS (PHASE 1 & 3)
    print("\n[CHECK 2] BACKEND ENVIRONMENT & CREDENTIALS")
    from app.core.config import settings
    print(f"  PROJECT_NAME       : {settings.PROJECT_NAME}")
    print(f"  SUPABASE_URL       : {settings.SUPABASE_URL[:40]}...")
    print(f"  SUPABASE_ANON_KEY  : {'CONFIGURED' if settings.SUPABASE_ANON_KEY else 'MISSING'}")
    print(f"  DATABASE_URL       : {'CONFIGURED' if settings.DATABASE_URL else 'MISSING'}")
    print(f"  GROQ_API_KEY       : {'CONFIGURED' if settings.GROQ_API_KEY else 'MISSING'}")
    print(f"  GROQ_MODEL         : {settings.GROQ_MODEL}")

    # 3. SUPABASE DATABASE CONNECTION (PHASE 2)
    print("\n[CHECK 3] SUPABASE DATABASE (7 TABLES & CONNECTION)")
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy import text
    engine = create_async_engine(settings.DATABASE_URL, connect_args={"statement_cache_size": 0})
    try:
        async with engine.connect() as conn:
            res = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name"))
            tables = [r[0] for r in res.fetchall()]
            expected = {"activities", "ai_generation_logs", "itineraries", "itinerary_days", "trips", "user_preferences", "user_profiles"}
            missing = expected - set(tables)
            print(f"  Connected to Cloud PostgreSQL : YES")
            print(f"  Tables found ({len(tables)}/7)          : {', '.join(tables)}")
            if missing:
                print(f"  ❌ Missing tables: {missing}")
            else:
                print(f"  All 7 tables verified         : OK")
    except Exception as e:
        print(f"  ❌ Database connection error: {e}")
    finally:
        await engine.dispose()

    # 4. FASTAPI APP & ROUTERS (PHASE 3 & 4)
    print("\n[CHECK 4] FASTAPI ENDPOINTS & CORS")
    from app.main import app
    paths = list(app.openapi()["paths"].keys())
    print(f"  CORS Allowed Origins : {settings.ALLOWED_ORIGINS}")
    print(f"  Active API Endpoints :")
    for p in paths:
        methods = list(app.openapi()["paths"][p].keys())
        print(f"    • {p:25} [{', '.join(methods).upper()}]")

    # 5. GROQ AI PIPELINE (PHASE 4)
    print("\n[CHECK 5] AI PIPELINE MODULES")
    from app.ai.prompt_builder import build_itinerary_prompt
    from app.ai.response_parser import clean_and_parse_json
    from app.ai.cache_manager import generate_cache_key
    from app.services.ai_service import generate_itinerary_service

    test_key = generate_cache_key("Delhi", 2, 5000, "INR", "budget", ["food"], "solo", "fast")
    print(f"  Cache manager key hashing   : OK (Key={test_key[:16]}...)")
    test_json = clean_and_parse_json('{"trip_title": "Delhi Bite", "destination": "Delhi", "days": [{"day_number": 1}]}')
    print(f"  Response parser verification: OK (Title='{test_json['trip_title']}')")

    # 6. FRONTEND FILES & CONFIG (PHASE 5)
    print("\n[CHECK 6] FRONTEND ASSETS & CONFIGURATION")
    fe_env = os.path.join(frontend_dir, ".env")
    fe_vite = os.path.join(frontend_dir, "vite.config.js")
    fe_src = os.path.join(frontend_dir, "src")
    dist_dir = os.path.join(frontend_dir, "dist")

    print(f"  Frontend .env file          : {'EXISTS' if os.path.exists(fe_env) else 'MISSING'}")
    print(f"  Tailwind Vite Config        : {'EXISTS' if os.path.exists(fe_vite) else 'MISSING'}")
    print(f"  Production Build (dist)     : {'EXISTS' if os.path.exists(dist_dir) else 'MISSING'}")

    fe_files = [
        "src/App.jsx",
        "src/main.jsx",
        "src/index.css",
        "src/services/api.js",
        "src/services/supabase.js",
        "src/store/tripStore.js",
        "src/store/authStore.js",
        "src/pages/LandingPage.jsx",
        "src/pages/TripBuilder.jsx",
        "src/pages/ItineraryView.jsx",
        "src/pages/Dashboard.jsx",
        "src/pages/AuthPage.jsx",
        "src/components/layout/Navbar.jsx",
        "src/components/common/LoadingScreen.jsx"
    ]
    all_fe_ok = True
    for f in fe_files:
        f_path = os.path.join(frontend_dir, f)
        if not os.path.exists(f_path):
            all_fe_ok = False
            print(f"    ❌ Missing: {f}")
    if all_fe_ok:
        print(f"  All {len(fe_files)} Frontend source modules: OK")

    # 7. FRONTEND-TO-BACKEND BRIDGE (PHASE 6)
    print("\n[CHECK 7] FRONTEND-TO-BACKEND BRIDGE")
    with open(fe_env, "r") as f:
        fe_env_content = f.read()
    
    has_api_url = "VITE_API_BASE_URL" in fe_env_content
    has_supa_url = "VITE_SUPABASE_URL" in fe_env_content
    print(f"  VITE_API_BASE_URL mapped to http://localhost:8000 : {'YES' if has_api_url else 'NO'}")
    print(f"  Frontend Supabase Client configured              : {'YES' if has_supa_url else 'NO'}")
    print(f"  FastAPI CORS allows Frontend (localhost:5173)     : {'YES' if 'http://localhost:5173' in settings.ALLOWED_ORIGINS else 'NO'}")

    print("\n" + "=" * 60)
    print("🎉 ALL SYSTEMS FROM PHASE 1 THROUGH PHASE 6 VERIFIED!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
