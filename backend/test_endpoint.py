import asyncio
import sys
from datetime import date, timedelta
sys.stdout.reconfigure(encoding='utf-8')

import httpx
from app.main import app

async def test_endpoint():
    print("Testing /itinerary/generate endpoint via ASGI...")
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Check health first
        h = await client.get("/health")
        print("Health status:", h.json())

        # Generate a 2-day trip to Agra
        start = date.today() + timedelta(days=5)
        end = start + timedelta(days=1)
        payload = {
            "destination": "Agra, Uttar Pradesh",
            "start_date": str(start),
            "end_date": str(end),
            "budget_total": 8000,
            "currency": "INR",
            "travel_style": "cultural",
            "interests": ["Taj Mahal", "Mughal architecture", "Petha sweets"],
            "group_type": "couple",
            "group_size": 2,
            "accommodation_preference": "hotel",
            "pace": "moderate"
        }

        print("Sending POST /itinerary/generate...")
        res = await client.post("/itinerary/generate", json=payload)
        print("HTTP Status Code:", res.status_code)
        
        if res.status_code == 200:
            data = res.json()
            print("Status         :", data.get("status"))
            print("Trip ID        :", data.get("trip_id"))
            print("Itinerary ID   :", data.get("itinerary_id"))
            print("Trip Title     :", data.get("itinerary", {}).get("trip_title"))
            print("Days count     :", len(data.get("itinerary", {}).get("days", [])))
            print("✅ ENDPOINT VERIFICATION SUCCESSFUL!")
        else:
            print("Error details  :", res.text)

if __name__ == "__main__":
    asyncio.run(test_endpoint())
