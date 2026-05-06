from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data_sources"
OUT = ROOT / "processed_data"

DRFA_FILE = SOURCE / "drfa_activation_history_by_location_2026_january_30.csv"
HISTORICAL_FILE = SOURCE / "aemkh_disaster_events.csv"


def parse_year(value: str) -> int | None:
    value = (value or "").strip()
    if not value:
        return None
    match = re.match(r"^(\d{4})", value)
    if match:
        return int(match.group(1))
    for fmt in ("%m/%d/%Y %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).year
        except ValueError:
            pass
    return None


def parse_number(value: str) -> float:
    value = (value or "").strip().replace(",", "")
    if not value:
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def normalise_hazard(value: str) -> str:
    text = (value or "").lower()
    if "flood" in text or "rainfall" in text or "monsoon" in text or "trough" in text:
        return "Flood / Rainfall"
    if "bushfire" in text or "fire" in text:
        return "Bushfire"
    if "cyclone" in text or "tropical low" in text:
        return "Cyclone / Tropical Low"
    if "storm" in text or "tornado" in text or "thunderstorm" in text:
        return "Storm"
    if "heat" in text:
        return "Heat"
    return "Other"


def historical_category(title: str) -> str:
    prefix = (title or "").split(" - ")[0].strip()
    corrections = {
        "Envionmental": "Environmental",
        "Cyclone Larry": "Cyclone",
    }
    if prefix.lower().startswith("cyclone"):
        return "Cyclone"
    return corrections.get(prefix, prefix or "Unknown")


def is_australian_record(lat: float, lon: float, regions: str) -> bool:
    return 112 <= lon <= 154 and -44 <= lat <= -10


def write_rows(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def clean_drfa() -> None:
    with DRFA_FILE.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    clean = []
    yearly = Counter()
    year_hazard = Counter()
    hazard_counts = Counter()
    state_counts = Counter()
    state_hazard = Counter()
    lga_counts = Counter()
    category_counts = Counter()

    for row in rows:
        year = parse_year(row.get("disaster_start_date", ""))
        if year is None:
            continue
        hazard_group = normalise_hazard(row.get("hazard_type", ""))
        state = row.get("STATE", "").strip()
        lga = row.get("Location_Name", "").strip()
        category = row.get("highest_drfa_category_group", "").strip() or "unknown"
        clean_row = {
            "year": year,
            "state": state,
            "location_name": lga,
            "location_code": row.get("Location_code", "").strip(),
            "event_name": row.get("event_name", "").strip(),
            "hazard_type": row.get("hazard_type", "").strip(),
            "hazard_group": hazard_group,
            "highest_drfa_category_group": category,
            "disaster_start_date": row.get("disaster_start_date", "").strip(),
        }
        clean.append(clean_row)
        yearly[year] += 1
        year_hazard[(year, hazard_group)] += 1
        hazard_counts[hazard_group] += 1
        state_counts[state] += 1
        state_hazard[(state, hazard_group)] += 1
        lga_counts[(lga, state)] += 1
        category_counts[category] += 1

    write_rows(
        OUT / "drfa_records_clean.csv",
        clean,
        [
            "year",
            "state",
            "location_name",
            "location_code",
            "event_name",
            "hazard_type",
            "hazard_group",
            "highest_drfa_category_group",
            "disaster_start_date",
        ],
    )
    write_rows(
        OUT / "drfa_yearly.csv",
        [{"year": year, "activations": count} for year, count in sorted(yearly.items())],
        ["year", "activations"],
    )
    write_rows(
        OUT / "drfa_year_hazard.csv",
        [
            {"year": year, "hazard_group": hazard, "activations": count}
            for (year, hazard), count in sorted(year_hazard.items())
        ],
        ["year", "hazard_group", "activations"],
    )
    write_rows(
        OUT / "drfa_hazard_counts.csv",
        [{"hazard_group": hazard, "activations": count} for hazard, count in hazard_counts.most_common()],
        ["hazard_group", "activations"],
    )
    write_rows(
        OUT / "drfa_state_counts.csv",
        [{"state": state, "activations": count} for state, count in state_counts.most_common()],
        ["state", "activations"],
    )
    state_code = {
        "Australian Capital Territory": "1",
        "New South Wales": "3",
        "Northern Territory": "4",
        "Queensland": "5",
        "South Australia": "6",
        "Tasmania": "7",
        "Victoria": "8",
        "Western Australia": "9",
    }
    state_abbr = {
        "Australian Capital Territory": "ACT",
        "New South Wales": "NSW",
        "Northern Territory": "NT",
        "Queensland": "QLD",
        "South Australia": "SA",
        "Tasmania": "TAS",
        "Victoria": "VIC",
        "Western Australia": "WA",
    }
    state_tile = {
        "Western Australia": (0, 1),
        "Northern Territory": (1, 0),
        "South Australia": (1, 1),
        "Queensland": (2, 0),
        "New South Wales": (2, 1),
        "Victoria": (2, 2),
        "Tasmania": (2, 3),
        "Australian Capital Territory": (3, 1),
    }
    write_rows(
        OUT / "drfa_state_map.csv",
        [
            {
                "state": state,
                "state_abbr": state_abbr.get(state, state),
                "state_code": state_code.get(state, ""),
                "tile_x": state_tile.get(state, ("", ""))[0],
                "tile_y": state_tile.get(state, ("", ""))[1],
                "activations": count,
            }
            for state, count in state_counts.most_common()
            if state in state_code
        ],
        ["state", "state_abbr", "state_code", "tile_x", "tile_y", "activations"],
    )
    write_rows(
        OUT / "drfa_state_hazard.csv",
        [
            {"state": state, "hazard_group": hazard, "activations": count}
            for (state, hazard), count in sorted(state_hazard.items())
        ],
        ["state", "hazard_group", "activations"],
    )
    write_rows(
        OUT / "drfa_top_lgas.csv",
        [
            {"location_name": lga, "state": state, "activations": count}
            for (lga, state), count in lga_counts.most_common(30)
        ],
        ["location_name", "state", "activations"],
    )
    write_rows(
        OUT / "drfa_category_counts.csv",
        [{"category": category, "activations": count} for category, count in category_counts.most_common()],
        ["category", "activations"],
    )


def clean_historical() -> None:
    natural_categories = {
        "Bushfire",
        "Cyclone",
        "Earthquake",
        "Environmental",
        "Flood",
        "Hail",
        "Landslide",
        "Severe Storm",
        "Tornado",
        "Tsunami",
    }
    impact_fields = [
        "Deaths",
        "Injuries",
        "Evacuated",
        "Homeless",
        "Insured Cost",
        "Home(s) destroyed",
        "Building(s) destroyed",
    ]
    with HISTORICAL_FILE.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    clean = []
    category_counts = Counter()
    decade_category = Counter()
    top_impact = []

    for row in rows:
        year = parse_year(row.get("startDate", ""))
        lat = parse_number(row.get("lat", ""))
        lon = parse_number(row.get("lon", ""))
        if year is None or lat == 0 or lon == 0:
            continue
        category = historical_category(row.get("title", ""))
        if category not in natural_categories:
            continue
        if not is_australian_record(lat, lon, row.get("regions", "")):
            continue
        deaths = parse_number(row.get("Deaths", ""))
        injuries = parse_number(row.get("Injuries", ""))
        evacuated = parse_number(row.get("Evacuated", ""))
        homeless = parse_number(row.get("Homeless", ""))
        insured_cost = parse_number(row.get("Insured Cost", ""))
        homes_destroyed = parse_number(row.get("Home(s) destroyed", ""))
        buildings_destroyed = parse_number(row.get("Building(s) destroyed", ""))
        impact_score = (
            deaths * 10
            + injuries * 2
            + evacuated * 0.05
            + homeless * 0.2
            + homes_destroyed * 2
            + buildings_destroyed * 2
        )
        decade = (year // 10) * 10
        clean_row = {
            "id": row.get("id", "").strip(),
            "title": row.get("title", "").strip(),
            "category": category,
            "year": year,
            "decade": decade,
            "start_date": row.get("startDate", "").strip(),
            "end_date": row.get("endDate", "").strip(),
            "lat": lat,
            "lon": lon,
            "regions": row.get("regions", "").strip(),
            "deaths": deaths,
            "injuries": injuries,
            "evacuated": evacuated,
            "homeless": homeless,
            "insured_cost": insured_cost,
            "homes_destroyed": homes_destroyed,
            "buildings_destroyed": buildings_destroyed,
            "impact_score": round(impact_score, 2),
            "url": row.get("url", "").strip(),
        }
        clean.append(clean_row)
        category_counts[category] += 1
        decade_category[(decade, category)] += 1
        if any(parse_number(row.get(field, "")) > 0 for field in impact_fields):
            top_impact.append(clean_row)

    write_rows(
        OUT / "historical_events_clean.csv",
        clean,
        [
            "id",
            "title",
            "category",
            "year",
            "decade",
            "start_date",
            "end_date",
            "lat",
            "lon",
            "regions",
            "deaths",
            "injuries",
            "evacuated",
            "homeless",
            "insured_cost",
            "homes_destroyed",
            "buildings_destroyed",
            "impact_score",
            "url",
        ],
    )
    write_rows(
        OUT / "historical_category_counts.csv",
        [{"category": category, "events": count} for category, count in category_counts.most_common()],
        ["category", "events"],
    )
    write_rows(
        OUT / "historical_decade_category.csv",
        [
            {"decade": decade, "category": category, "events": count}
            for (decade, category), count in sorted(decade_category.items())
        ],
        ["decade", "category", "events"],
    )
    write_rows(
        OUT / "historical_top_impact_events.csv",
        sorted(top_impact, key=lambda row: row["impact_score"], reverse=True)[:30],
        [
            "id",
            "title",
            "category",
            "year",
            "lat",
            "lon",
            "regions",
            "deaths",
            "injuries",
            "evacuated",
            "homeless",
            "homes_destroyed",
            "buildings_destroyed",
            "impact_score",
            "url",
        ],
    )


def write_aihw_summary() -> None:
    rows = [
        {"metric": "Hospitalisations", "period": "2023-24", "value": 815, "note": "Forces of nature injuries"},
        {"metric": "Deaths", "period": "2022-23", "value": 68, "note": "Forces of nature injuries"},
        {"metric": "Male hospitalisations", "period": "2023-24", "value": 552, "note": "67% of hospitalisations"},
        {"metric": "Male deaths", "period": "2022-23", "value": 41, "note": "60% of deaths"},
        {"metric": "Age 65+ hospitalisations", "period": "2023-24", "value": 299, "note": "High burden age group"},
        {"metric": "Summer injury share", "period": "2023-24", "value": 40, "note": "Percent of injuries in summer"},
    ]
    write_rows(OUT / "aihw_forces_of_nature_summary.csv", rows, ["metric", "period", "value", "note"])


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    clean_drfa()
    clean_historical()
    write_aihw_summary()
    print(f"Processed data written to {OUT}")


if __name__ == "__main__":
    main()
