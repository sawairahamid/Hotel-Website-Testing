"""
Utility / Helper Functions
Shared test data, oracle functions, and boundary helpers.
"""
from datetime import date, timedelta

# ── Preset Users (Hotel Planisphere built-in accounts) ────────────────────────
PREMIUM_USER   = {"email": "clark@example.com",  "password": "password"}
NORMAL_USER    = {"email": "diana@example.com",  "password": "pass1234"}
PREMIUM_USER_2 = {"email": "ororo@example.com",  "password": "pa55w0rd!"}
NORMAL_USER_2  = {"email": "miles@example.com",  "password": "pass-pass"}

# ── Invalid Credentials ───────────────────────────────────────────────────────
INVALID_USER   = {"email": "nobody@fake.com",    "password": "wrongpass"}
WRONG_PASSWORD = {"email": "clark@example.com",  "password": "badpassword"}

# ── Base URL ──────────────────────────────────────────────────────────────────
BASE_URL = "https://hotel-example-site.takeyaqa.dev/en-US"

# ── Price Add-ons (from site documentation) ───────────────────────────────────
BREAKFAST_ADDON_PER_PERSON_PER_NIGHT = 1000
EARLY_CHECKIN_FLAT                   = 1000
SIGHTSEEING_FLAT                     = 500


def calculate_expected_price(base_rate_per_night, nights, head_count,
                              breakfast=False, early_checkin=False, sightseeing=False):
    """
    Oracle function: deterministic price calculation.
    Mirrors the hotel site's pricing logic for assertion comparisons.
    """
    total = base_rate_per_night * nights * head_count
    if breakfast:
        total += BREAKFAST_ADDON_PER_PERSON_PER_NIGHT * nights * head_count
    if early_checkin:
        total += EARLY_CHECKIN_FLAT
    if sightseeing:
        total += SIGHTSEEING_FLAT
    return total


def future_date(days_ahead=7, fmt="%Y/%m/%d"):
    """Returns a future date string for booking forms."""
    return (date.today() + timedelta(days=days_ahead)).strftime(fmt)


def boundary_values(min_val, max_val):
    """Returns standard BVA test values for a numeric field."""
    return {
        "below_min": min_val - 1,
        "min":       min_val,
        "valid_mid": (min_val + max_val) // 2,
        "max":       max_val,
        "above_max": max_val + 1,
    }
