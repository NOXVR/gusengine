# backend/routes/vehicle_linter.py
# V10 FIREWALL: Pre-LLM vehicle mismatch detection
# Scans user query text for make/model/year mentions that don't match the active vehicle.
# Pure text matching — no AI, no cost, runs before embedding/search/LLM.
import re
import logging

logger = logging.getLogger(__name__)

# Common aliases and abbreviations for known makes/models.
# Keyed by the canonical value in vehicle_registry.json.
_MAKE_ALIASES: dict[str, list[str]] = {
    "Ford": ["ford"],
    "Mercedes-Benz": ["mercedes", "merc", "benz", "mercedes-benz", "mb"],
    "Chevrolet": ["chevy", "chevrolet"],
    "Dodge": ["dodge"],
    "Plymouth": ["plymouth"],
    "Pontiac": ["pontiac"],
    "Toyota": ["toyota"],
    "Honda": ["honda"],
    "BMW": ["bmw"],
    "Porsche": ["porsche"],
    "Volkswagen": ["vw", "volkswagen"],
    "Audi": ["audi"],
}

_MODEL_ALIASES: dict[str, list[str]] = {
    "Mustang": ["mustang", "stang"],
    "450SL": ["450sl", "450 sl", "r107", "w107"],
    "Camaro": ["camaro"],
    "Corvette": ["corvette", "vette"],
    "Charger": ["charger"],
    "Challenger": ["challenger"],
    "GTO": ["gto"],
    "Firebird": ["firebird"],
}


def _build_vehicle_keywords(vehicle: dict) -> set[str]:
    """Build set of lowercase keywords that identify a specific vehicle."""
    keywords = set()
    make = vehicle.get("make", "")
    model = vehicle.get("model", "")
    year = vehicle.get("year")

    # Add canonical make/model (lowercased)
    if make:
        keywords.add(make.lower())
    if model:
        keywords.add(model.lower())

    # Add all known aliases for this make
    for canonical, aliases in _MAKE_ALIASES.items():
        if canonical.lower() == make.lower():
            keywords.update(aliases)

    # Add all known aliases for this model
    for canonical, aliases in _MODEL_ALIASES.items():
        if canonical.lower() == model.lower():
            keywords.update(aliases)

    # Year as string
    if year:
        keywords.add(str(year))

    return keywords


def lint_vehicle_mismatch(
    query: str,
    active_vehicle: dict,
    all_vehicles: list[dict],
) -> dict | None:
    """Scan query for vehicle mentions that don't match the active vehicle.

    Returns None if no mismatch detected.
    Returns a dict with warning details if a cross-vehicle mention is found.
    """
    query_lower = query.lower()

    # Build keyword sets for ALL vehicles
    active_keywords = _build_vehicle_keywords(active_vehicle)
    active_year = active_vehicle.get("year")
    active_make = active_vehicle.get("make", "").lower()
    active_model = active_vehicle.get("model", "").lower()

    # Check each OTHER vehicle for keyword matches in the query
    for other_vehicle in all_vehicles:
        if other_vehicle["id"] == active_vehicle["id"]:
            continue  # Skip the active vehicle

        other_keywords = _build_vehicle_keywords(other_vehicle)
        other_make = other_vehicle.get("make", "").lower()
        other_model = other_vehicle.get("model", "").lower()
        other_year = other_vehicle.get("year")

        # Check for make/model matches against OTHER vehicles
        matched_terms = []
        for kw in other_keywords:
            if kw == str(other_year):
                continue  # Handle years separately below
            # Word boundary match to avoid false positives (e.g., "ford" in "afford")
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, query_lower):
                # Make sure this keyword does NOT also belong to the active vehicle
                if kw not in active_keywords:
                    matched_terms.append(kw)

        # Check for year mismatch — only flag if a different year explicitly appears
        year_matches = re.findall(r'\b(19\d{2}|20\d{2})\b', query_lower)
        mismatched_years = []
        for ym in year_matches:
            year_int = int(ym)
            if year_int != active_year and year_int == other_year:
                mismatched_years.append(ym)

        if matched_terms or mismatched_years:
            all_detected = matched_terms + mismatched_years
            active_label = f"{active_vehicle.get('year', '')} {active_vehicle.get('make', '')} {active_vehicle.get('model', '')}"
            other_label = f"{other_vehicle.get('year', '')} {other_vehicle.get('make', '')} {other_vehicle.get('model', '')}"

            logger.warning(
                f"VEHICLE MISMATCH FIREWALL: Query mentions {all_detected} "
                f"(maps to {other_label}) but active vehicle is {active_label}"
            )

            return {
                "detected": other_label.strip(),
                "detected_terms": all_detected,
                "active": active_label.strip(),
                "warning": (
                    f"⚠️ VEHICLE MISMATCH: Your question mentions "
                    f"\"{', '.join(all_detected)}\" which belongs to the "
                    f"{other_label.strip()}. You currently have the "
                    f"{active_label.strip()} selected. "
                    f"Please switch to the correct vehicle, or if this was "
                    f"intentional, click 'Continue Anyway' to proceed."
                ),
                "detail": (
                    f"Pre-LLM firewall detected cross-vehicle terms {all_detected} "
                    f"in query. Active vehicle: {active_label.strip()}, "
                    f"detected vehicle: {other_label.strip()}."
                ),
            }

    # Also check for years that don't match ANY registered vehicle
    # (catches cases like "my 1972 Mustang" when only 1965 is registered)
    year_matches = re.findall(r'\b(19\d{2}|20\d{2})\b', query_lower)
    for ym in year_matches:
        year_int = int(ym)
        if year_int != active_year:
            # Check if any registered vehicle has this year
            known_years = {v.get("year") for v in all_vehicles}
            if year_int not in known_years:
                # Unknown year mentioned — still flag it if it's clearly a car year
                # Only flag if year is in a reasonable car range (1900-2030)
                if 1900 <= year_int <= 2030:
                    active_label = f"{active_vehicle.get('year', '')} {active_vehicle.get('make', '')} {active_vehicle.get('model', '')}"
                    logger.warning(
                        f"VEHICLE MISMATCH FIREWALL: Query mentions year {ym} "
                        f"which does not match active vehicle year {active_year}"
                    )
                    return {
                        "detected": f"Year {ym} (unknown vehicle)",
                        "detected_terms": [ym],
                        "active": active_label.strip(),
                        "warning": (
                            f"⚠️ YEAR MISMATCH: Your question mentions the year "
                            f"{ym}, but the selected vehicle is a "
                            f"{active_label.strip()}. If you meant to ask about "
                            f"a different year, please check your vehicle selection."
                        ),
                        "detail": (
                            f"Pre-LLM firewall detected year {ym} in query. "
                            f"Active vehicle year: {active_year}."
                        ),
                    }

    return None
