import asyncio
import sys
import json
from datetime import date, timedelta
sys.stdout.reconfigure(encoding='utf-8')

from app.services.ai_service import generate_itinerary_service

async def main():
    print("==================================================")
    print("🚀 TESTING AI PIPELINE (PHASE 4)")
    print("==================================================")
    
    destination = "Jaipur, Rajasthan"
    start_date = date.today() + timedelta(days=10)
    end_date = start_date + timedelta(days=1)  # 2-day trip for fast testing
    budget_total = 12000.0
    currency = "INR"
    travel_style = "cultural"
    interests = ["historical forts", "local Rajasthani food", "handicrafts"]
    group_type = "couple"
    group_size = 2
    pace = "moderate"

    print(f"\n1. Submitting test request:")
    print(f"   Destination: {destination}")
    print(f"   Duration   : 2 Days ({start_date} to {end_date})")
    print(f"   Budget     : {budget_total} {currency}")
    print(f"   Interests  : {interests}")
    print("\n2. Calling Groq AI model...")

    try:
        itinerary, metadata = await generate_itinerary_service(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget_total=budget_total,
            currency=currency,
            travel_style=travel_style,
            interests=interests,
            group_type=group_type,
            group_size=group_size,
            pace=pace
        )

        print("\n✅ AI Pipeline SUCCESS!")
        print("--------------------------------------------------")
        print(f"Model used       : {metadata.get('model_used')}")
        print(f"Time taken       : {metadata.get('generation_time_ms')} ms")
        print(f"Tokens consumed  : In={metadata.get('tokens_input')}, Out={metadata.get('tokens_output')}")
        print(f"Cached           : {metadata.get('cached')}")
        print("--------------------------------------------------")
        print(f"Trip Title       : {itinerary.get('trip_title')}")
        print(f"Destination      : {itinerary.get('destination')}")
        print(f"Estimated Cost   : {itinerary.get('estimated_total_cost')} {itinerary.get('currency')}")
        print(f"Total Days       : {itinerary.get('total_days')}")
        
        days = itinerary.get("days", [])
        print(f"\nGenerated {len(days)} Days of Plans:")
        for day in days:
            print(f"\n  📅 Day {day.get('day_number')} - Theme: {day.get('theme')} (Est. Cost: {day.get('estimated_day_cost')})")
            for act in day.get("activities", []):
                print(f"     • [{act.get('time_slot')}] {act.get('name')} ({act.get('activity_type')}) - ₹{act.get('estimated_cost')}")
                print(f"       Loc: {act.get('location')}")
                print(f"       Tip: {act.get('tips')}")

        # Test cache hit
        print("\n3. Testing Cache (Sending identical request)...")
        cached_itin, cached_meta = await generate_itinerary_service(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget_total=budget_total,
            currency=currency,
            travel_style=travel_style,
            interests=interests,
            group_type=group_type,
            group_size=group_size,
            pace=pace
        )
        print(f"✅ Cache Hit test: cached={cached_meta.get('cached')}, response_time={cached_meta.get('generation_time_ms')}ms")
        print("\n🎉 PHASE 4 AI PIPELINE IS 100% OPERATIONAL!")

    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
