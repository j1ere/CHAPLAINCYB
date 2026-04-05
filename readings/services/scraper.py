import requests
import re
from bs4 import BeautifulSoup
from datetime import date

def fetch_readings(target_date: date = None) -> dict:
    """
    Fetch and clean daily readings from USCCB.
    
    Args:
        target_date: date object. Defaults to today.
    
    Returns:
        dict with keys: date, feast, lectionary, readings (list)
    """
    if target_date is None:
        target_date = date.today()

    url = f"https://bible.usccb.org/bible/readings/{target_date.strftime('%m%d%y')}.cfm"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DailyReadingsScraper/1.0)"
    }
    
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, "html.parser")
    return parse_readings(soup, target_date)


def clean_text(raw: str) -> str:
    """Clean raw scraped text into readable format."""
    # Replace non-breaking spaces with regular spaces
    text = raw.replace("\xa0", " ")
    
    # Normalize all whitespace runs (tabs, multiple spaces) to single space
    text = re.sub(r"[ \t]+", " ", text)
    
    # Strip trailing whitespace on each line
    lines = [line.rstrip() for line in text.splitlines()]
    
    # Collapse 3+ consecutive blank lines into 2 (paragraph break)
    cleaned_lines = []
    blank_count = 0
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                cleaned_lines.append("")
        else:
            blank_count = 0
            cleaned_lines.append(line)
    
    # Strip leading/trailing blank lines from result
    text = "\n".join(cleaned_lines).strip()
    return text


def parse_readings(soup: BeautifulSoup, target_date: date) -> dict:
    """Extract and structure all readings from parsed HTML."""
    
    # --- Metadata ---
    feast_tag = soup.find("h2")
    # The real feast name is the h2 that isn't visually-hidden
    feast = ""
    for h2 in soup.find_all("h2"):
        if "visually-hidden" not in h2.get("class", []):
            feast = h2.get_text(strip=True)
            break

    lectionary_tag = soup.find("p", string=re.compile(r"Lectionary"))
    lectionary = lectionary_tag.get_text(strip=True) if lectionary_tag else ""

    # --- Readings ---
    readings = []
    
    for block in soup.find_all("div", class_="innerblock"):
        h3 = block.find("h3", class_="name")
        if not h3:
            continue
        
        section_name = h3.get_text(strip=True)
        if not section_name:
            continue
        
        address_tag = block.find("div", class_="address")
        reference = address_tag.get_text(strip=True) if address_tag else ""
        
        # Get reference URL if available
        ref_link = address_tag.find("a") if address_tag else None
        reference_url = ref_link["href"].strip() if ref_link and ref_link.get("href") else ""
        
        body = block.find("div", class_="content-body")
        raw_text = body.get_text(separator="\n") if body else ""
        text = clean_text(raw_text)
        
        readings.append({
            "section": section_name,
            "reference": reference,
            "reference_url": reference_url,
            "text": text
        })
    
    return {
        "date": target_date.isoformat(),
        "feast": feast,
        "lectionary": lectionary,
        "readings": readings
    }


def display_readings(data: dict):
    """Pretty-print the readings to console."""
    print(f"\n{'='*60}")
    print(f"  {data['date']}  |  {data['feast']}")
    print(f"  {data['lectionary']}")
    print(f"{'='*60}\n")
    
    for r in data["readings"]:
        print(f"--- {r['section']} ---")
        print(f"📖 {r['reference']}")
        print()
        print(r["text"])
        print("\n")


# --- Run ---
if __name__ == "__main__":
    data = fetch_readings()  # today, or pass: date(2026, 4, 3)
    display_readings(data)
    
    # Access individual readings programmatically
    for r in data["readings"]:
        print(f"{r['section']}: {len(r['text'])} chars")