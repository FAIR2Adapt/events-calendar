import csv
import json
import re
from datetime import datetime, timedelta

# Mapping of event types to colors
type_colors = {
    "Workshop": "#1f77b4",
    "Training event": "#ff7f0e",
    "Conference": "#2ca02c",
    "Tutorial": "#d62728",
    "Demo": "#9467bd",
    "Webinar": "#17becf"
}

def parse_date(date_str):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

events = []
with open('input.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        start = parse_date(row["Start date"])
        end = parse_date(row["End date"])

        if not start:
            continue

        # Add one day to end if different from start (FullCalendar is exclusive)
        if end and end > start:
            end = end + timedelta(days=1)
        else:
            end = start

        title_parts = [
            f"({row['Type of activity']})" if row["Type of activity"] else "",
            f"\nLocation: {row['Location (city)']}, {row['Location (country)']}" if row["Location (city)"] or row["Location (country)"] else "",
            f"\nSpeaker/Participant: {row['Speaker / Participant / Organiser']}" if row["Speaker / Participant / Organiser"] else "",
        ]
        title = row["Activity name (event, publication, tutorial, news article, etc.)"]
        description = ";".join(part for part in title_parts if part)
        evidence = row['Evidence'] if row["Evidence"] else ""
        url_start = evidence.find("http")
        if url_start == -1:
           url = "https://fair2adapt-eosc.eu"
        else:
            url_end = evidence[url_start:].find(" ")
            url = evidence[url_start:url_end]

        # Get color based on first label
        first_type = row["Type of activity"].split(",")[0].strip()
        color = type_colors.get(first_type, "#888")  # Default gray
        print(first_type, color)

        event = {
            "title": title.strip(),
            "start": start.isoformat(),
            "end": end.isoformat(),
            "description": description.strip(),
            "url": url.strip(),
            "type": first_type
        }
        events.append(event)

events.sort(key=lambda e: e["start"])
# Write to events.json
with open('events.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(events, jsonfile, indent=2, ensure_ascii=False)

print(f" {len(events)} events written to events.json")

