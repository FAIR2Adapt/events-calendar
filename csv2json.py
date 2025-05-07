import csv
import json
from datetime import datetime, timedelta

# Map event types to colors
TYPE_COLORS = {
    "Workshop": "blue",
    "Webinar": "orange",
    "Training event": "green",
    "Conference": "red",
    "Publication": "purple",
    "Other": "gray"
}

def parse_date(date_str):
    """Convert 'dd/mm/yyyy' to 'yyyy-mm-dd'."""
    try:
        return datetime.strptime(date_str.strip(), "%d/%m/%Y").date().isoformat()
    except ValueError:
        return None

def get_color(activity_type):
    return TYPE_COLORS.get(activity_type.strip(), TYPE_COLORS["Other"])

events = []

with open("input.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        start = parse_date(row["Start date"])
        end = parse_date(row["End date"])
        if not start:
            continue  # Skip invalid rows

        # FullCalendar requires end date to be exclusive for multi-day events
        if start == end or not end:
            event_end = start
        else:
            event_end = (datetime.strptime(end, "%Y-%m-%d").date() + timedelta(days=1)).isoformat()

        event = {
            "title": row['Activity name (event, publication, tutorial, news article, etc.)'].strip(),
            "start": start,
            "end": event_end,
            "backgroundColor": get_color(row["Type of activity"]),
            "extendedProps": {
                "partner": row["Partner"],
                "role": row["Speaker / Participant / Organiser"],
                "type": row["Type of activity"],
                "status": row["Status"],
                "location": f"{row['Location (city)']} ({row['Location (country)']})",
                "audienceSize": row["Audience size"],
                "evidence": row["Evidence"],
                "notes": row["Notes"]
            }
        }
        events.append(event)

# Write to JSON file
with open("events.json", "w", encoding='utf-8') as jsonfile:
    json.dump(events, jsonfile, indent=2, ensure_ascii=False)

print(f"Successfully wrote {len(events)} events to events.json")
