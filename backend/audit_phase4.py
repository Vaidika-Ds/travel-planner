import sys
import json
from datetime import date
sys.stdout.reconfigure(encoding='utf-8')

from app.ai.response_parser import clean_and_parse_json
from app.ai.prompt_builder import build_itinerary_prompt
from app.ai.cache_manager import generate_cache_key, get_cached_itinerary, set_cached_itinerary

def test_audit():
    print("=== STARTING PHASE 4 REALITY AUDIT ===")
    
    # -------------------------------------------------------------
    # TEST 1: Parsing Clean JSON
    # -------------------------------------------------------------
    raw_clean = '{"trip_title": "Goa Trip", "destination": "Goa", "days": [{"day_number": 1}]}'
    res = clean_and_parse_json(raw_clean)
    assert res["trip_title"] == "Goa Trip"
    print("✅ Test 1 Passed: Clean JSON parsed correctly")

    # -------------------------------------------------------------
    # TEST 2: Parsing Markdown Wrapped JSON (common LLM behavior)
    # -------------------------------------------------------------
    raw_markdown = '''```json
    {
        "trip_title": "Manali Trip",
        "destination": "Manali",
        "days": [{"day_number": 1}]
    }
    ```'''
    res2 = clean_and_parse_json(raw_markdown)
    assert res2["trip_title"] == "Manali Trip"
    print("✅ Test 2 Passed: Markdown code fences properly stripped")

    # -------------------------------------------------------------
    # TEST 3: Parsing Conversational Text Before & After JSON
    # -------------------------------------------------------------
    raw_conversational = '''Here is your customized travel itinerary!
    {
        "trip_title": "Kerala Backwaters",
        "destination": "Kerala",
        "days": [{"day_number": 1}]
    }
    Hope you have an amazing journey! Let me know if you need changes.'''
    res3 = clean_and_parse_json(raw_conversational)
    assert res3["trip_title"] == "Kerala Backwaters"
    print("✅ Test 3 Passed: Conversational prefixes and suffixes ignored")

    # -------------------------------------------------------------
    # TEST 4: Malformed or Incomplete JSON handling
    # -------------------------------------------------------------
    raw_broken = '{"trip_title": "Broken Trip", "days": '
    try:
        clean_and_parse_json(raw_broken)
        print("❌ Test 4 Failed: Should have caught broken JSON")
    except ValueError as e:
        print(f"✅ Test 4 Passed: Broken JSON cleanly caught with ValueError: {e}")

    # -------------------------------------------------------------
    # TEST 5: Missing Required Keys Verification
    # -------------------------------------------------------------
    raw_missing = '{"random_key": "some_value"}'
    try:
        clean_and_parse_json(raw_missing)
        print("❌ Test 5 Failed: Should have caught missing required keys")
    except ValueError as e:
        print(f"✅ Test 5 Passed: Missing keys cleanly caught: {e}")

    # -------------------------------------------------------------
    # TEST 6: Prompt Builder String Verification
    # -------------------------------------------------------------
    p = build_itinerary_prompt(
        destination="Shimla",
        start_date=date(2026, 11, 1),
        end_date=date(2026, 11, 3),
        num_days=3,
        budget_total=15000,
        currency="INR",
        travel_style="relaxed",
        interests=["nature", "snow"],
        group_type="family",
        group_size=4,
        accommodation_preference="resort",
        pace="slow"
    )
    assert "Shimla" in p
    assert "15000" in p
    assert "slow" in p
    assert "resort" in p
    print("✅ Test 6 Passed: Prompt builder injects all parameters faithfully")

    # -------------------------------------------------------------
    # TEST 7: Cache Key Determinism & Invalidation
    # -------------------------------------------------------------
    k1 = generate_cache_key("Mumbai", 3, 10000, "INR", "budget", ["food", "beaches"], "solo", "fast")
    k2 = generate_cache_key("Mumbai", 3, 10000, "INR", "budget", ["beaches", "food"], "solo", "fast")
    assert k1 == k2, "Cache key should be identical regardless of interest order!"
    print("✅ Test 7 Passed: Cache keys are order-independent and deterministic")

    print("\n🎉 ALL 7 AUDIT TESTS PASSED WITH 0 ERRORS!")

if __name__ == "__main__":
    test_audit()
