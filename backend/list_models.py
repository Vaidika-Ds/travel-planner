import asyncio
import sys
import httpx
sys.stdout.reconfigure(encoding='utf-8')

async def list_models():
    from app.core.config import settings
    headers = {"Authorization": f"Bearer {settings.GROQ_API_KEY}"}
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get("https://api.groq.com/openai/v1/models", headers=headers)
        data = r.json()
        print("Available Groq models:")
        for m in sorted(data.get("data", []), key=lambda x: x["id"]):
            print(" -", m["id"])

asyncio.run(list_models())
