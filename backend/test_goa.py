import asyncio
import sys
from datetime import date, timedelta
sys.stdout.reconfigure(encoding='utf-8')

from app.services.ai_service import generate_itinerary_service

async def test():
    dest = "Goa, India"
    start = date(2026, 11, 15)
    end = start + timedelta(days=2)  # 3 days total
    print("Testing 3-Day Trip Generation for Goa...")

    itin, meta = await generate_itinerary_service(
        destination=dest,
        start_date=start,
        end_date=end,
        budget_total=20000,
        currency="INR",
        travel_style="relaxed",
        interests=["beaches", "seafood", "sunsets"],
        pace="moderate"
    )

    print("Title      :", itin.get("trip_title"))
    print("Total days :", len(itin.get("days", [])))
    print("Est. Cost  :", itin.get("estimated_total_cost"))
    print("Tokens Out :", meta.get("tokens_output"))
    print("Latency    :", meta.get("generation_time_ms"), "ms")
    assert len(itin.get("days", [])) == 3, f"Expected 3 days, got {len(itin.get('days', []))}"
    print("✅ 3-DAY ITINERARY GENERATION & PARSING VERIFIED 100%!")

if __name__ == "__main__":
    asyncio.run(test())
