import sys
sys.stdout.reconfigure(encoding='utf-8')

from app.core.config import settings

print("=== ENV CHECK ===")
print("PROJECT_NAME :", settings.PROJECT_NAME)
print("SUPABASE_URL :", settings.SUPABASE_URL[:40] + "..." if settings.SUPABASE_URL else "MISSING")
print("SUPABASE_ANON_KEY:", "SET" if settings.SUPABASE_ANON_KEY else "MISSING")
print("SUPABASE_SERVICE_KEY:", "SET" if settings.SUPABASE_SERVICE_ROLE_KEY else "MISSING")
print("DATABASE_URL :", "SET" if settings.DATABASE_URL else "MISSING")
print("GROQ_API_KEY :", "SET" if settings.GROQ_API_KEY else "MISSING")
print("GROQ_MODEL   :", settings.GROQ_MODEL)
print("ENVIRONMENT  :", settings.ENVIRONMENT)
print("=================")
