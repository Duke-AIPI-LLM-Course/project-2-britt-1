from langchain.tools import tool
import requests
from bs4 import BeautifulSoup

@tool
def get_duke_events(_: str) -> str:
    """
    Scrapes recent events from Duke's public calendar website.
    """
    url = "https://calendar.duke.edu"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    events = soup.select(".event-title a")

    if not events:
        return "No events found."

    return "\n".join([e.get_text(strip=True) for e in events[:5]])
