import requests
from bs4 import BeautifulSoup

urls = [
    "https://masters.pratt.duke.edu/ai/",
    "https://masters.pratt.duke.edu/ai/overview/",
    "https://masters.pratt.duke.edu/ai/degree/",
    "https://masters.pratt.duke.edu/ai/courses/",
    "https://masters.pratt.duke.edu/ai/outcomes/",
    "https://masters.pratt.duke.edu/ai/certificate/",
    "https://masters.pratt.duke.edu/people?s=&department=artificial-intelligence&group=faculty&submit=Filter",
    "http://masters.pratt.duke.edu/ai/leadership-staff/",
    "https://masters.pratt.duke.edu/ai/news-events/",
    "https://masters.pratt.duke.edu/life/students/",
    "https://masters.pratt.duke.edu/apply/"
]

all_text = ""

for url in urls:
    try:
        print(f"Scraping {url}")
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Strip out script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text(separator="\n", strip=True)
        all_text += f"\n\n==== {url} ====\n\n{text}"
    except Exception as e:
        all_text += f"\n\n==== {url} ====\n\n[Error fetching page: {e}]"

# Save the full text to your vectorstore
with open("vectorstore/data/ai_meng.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("Saved all scraped content to vectorstore/data/ai_meng.txt")
