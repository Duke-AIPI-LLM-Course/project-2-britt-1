from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from datetime import datetime

@tool
def get_duke_events(query: str) -> str:
    """Get a list of upcoming events at Duke University."""
    url = "https://calendar.duke.edu"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Error fetching events: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    event_blocks = soup.select(".event-info")  # each event block with title + time
    for block in event_blocks:
        title_el = block.select_one("h3 > a")
        time_el = block.select_one(".event-time")

        if not title_el or not time_el:
            continue

        title = title_el.get_text(strip=True)
        time_text = time_el.get_text(strip=True)

        try:
            # Try parsing the date string
            event_date = datetime.strptime(time_text, "%A, %B %d, %Y - %I:%M%p")
            if event_date >= datetime.now():
                events.append(f"{title} — {event_date.strftime('%b %d, %Y at %I:%M %p')}")
        except Exception:
            # If date parsing fails, skip it
            continue

        if len(events) >= 5:
            break

    return "\n".join(events) if events else "No upcoming events found."
