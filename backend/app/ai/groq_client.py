import asyncio
import httpx
import time
from typing import Dict, Any, Tuple
from app.core.config import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def call_groq_api(prompt: str, retries: int = 2) -> Tuple[str, Dict[str, Any]]:
    """
    Sends the prompt to Groq API with automatic retries and returns:
    (raw_response_text, metadata_dict)
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in environment.")

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a professional travel planner. You must return only valid, well-formed JSON. Do not include markdown or conversational commentary."
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 8192,
        "response_format": {"type": "json_object"}  # Forces JSON mode
    }

    last_error = None
    for attempt in range(retries + 1):
        try:
            start_time = time.time()
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(GROQ_API_URL, headers=headers, json=payload)
                elapsed_ms = int((time.time() - start_time) * 1000)

                if response.status_code == 200:
                    data = response.json()
                    raw_text = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    metadata = {
                        "model_used": data.get("model", settings.GROQ_MODEL),
                        "tokens_input": usage.get("prompt_tokens", 0),
                        "tokens_output": usage.get("completion_tokens", 0),
                        "generation_time_ms": elapsed_ms
                    }
                    return raw_text, metadata
                else:
                    last_error = f"Groq API Error [{response.status_code}]: {response.text}"
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            last_error = f"Network/Timeout error: {str(e)}"

        # If we reached here, attempt failed. Wait briefly before retrying
        if attempt < retries:
            await asyncio.sleep(2)

    raise RuntimeError(last_error or "Failed to call Groq API after retries.")
