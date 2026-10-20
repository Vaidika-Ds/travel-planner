import asyncio
import sys
import httpx
sys.stdout.reconfigure(encoding='utf-8')

async def test_groq():
    from app.core.config import settings
    print("Testing Groq AI connection...")
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [{"role": "user", "content": "Say: Groq connected!"}],
        "max_tokens": 20,
        "temperature": 0.0
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload
            )
            data = response.json()
            if response.status_code == 200:
                msg = data["choices"][0]["message"]["content"]
                tokens = data["usage"]["total_tokens"]
                print(f"Groq CONNECTED! Response: {msg}")
                print(f"Tokens used: {tokens}")
                print(f"Model: {data['model']}")
            else:
                print(f"Groq ERROR {response.status_code}: {data}")
        except Exception as e:
            print(f"Groq FAILED: {e}")

asyncio.run(test_groq())
