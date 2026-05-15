import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, date
from zoneinfo import ZoneInfo


def build_usccb_url(target_date: date) -> str:
    """
    Build the USCCB daily readings URL.

    Example:
    2026-05-18 ->
    https://bible.usccb.org/bible/readings/051826.cfm
    """

    month_day_year = target_date.strftime("%m%d%y")

    return (
        "https://bible.usccb.org/bible/readings/"
        f"{month_day_year}.cfm"
    )


def fetch_readings(target_date: date = None) -> dict:
    """
    Fetch and clean daily readings from USCCB.

    Args:
        target_date: date object.
                     Defaults to today's Nairobi date.

    Returns:
        dict containing:
            - date
            - feast
            - lectionary
            - readings
    """

    # Use Kenya timezone explicitly
    if target_date is None:
        target_date = datetime.now(
            ZoneInfo("Africa/Nairobi")
        ).date()

    url = build_usccb_url(target_date)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(compatible; DailyReadingsScraper/1.0)"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return parse_readings(soup, target_date)


def clean_text(raw: str) -> str:
    """
    Clean scraped text while preserving meaningful formatting.
    """

    # Replace non-breaking spaces
    text = raw.replace("\xa0", " ")

    # Normalize spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove trailing spaces
    lines = [line.rstrip() for line in text.splitlines()]

    cleaned_lines = []
    blank_run = 0

    for line in lines:

        if line.strip() == "":
            blank_run += 1

            # Allow max one separator blank line
            if blank_run <= 2:
                cleaned_lines.append("")

        else:
            blank_run = 0
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def parse_readings(
    soup: BeautifulSoup,
    target_date: date
) -> dict:
    """
    Parse all readings from the HTML page.
    """

    # ---------------- Metadata ---------------- #

    feast = ""

    for h2 in soup.find_all("h2"):

        if "visually-hidden" not in h2.get("class", []):

            feast = h2.get_text(strip=True)
            break

    lectionary_tag = soup.find(
        "p",
        string=re.compile(r"Lectionary")
    )

    lectionary = (
        lectionary_tag.get_text(strip=True)
        if lectionary_tag
        else ""
    )

    # ---------------- Readings ---------------- #

    readings = []

    for block in soup.find_all(
        "div",
        class_="innerblock"
    ):

        h3 = block.find("h3", class_="name")

        if not h3:
            continue

        section_name = h3.get_text(strip=True)

        if not section_name:
            continue

        address_tag = block.find(
            "div",
            class_="address"
        )

        reference = (
            address_tag.get_text(strip=True)
            if address_tag
            else ""
        )

        ref_link = (
            address_tag.find("a")
            if address_tag
            else None
        )

        reference_url = (
            ref_link["href"].strip()
            if ref_link and ref_link.get("href")
            else ""
        )

        body = block.find(
            "div",
            class_="content-body"
        )

        raw_text = (
            body.get_text(separator="\n")
            if body
            else ""
        )

        text = clean_text(raw_text)

        readings.append(
            {
                "section": section_name,
                "reference": reference,
                "reference_url": reference_url,
                "text": text,
            }
        )

    return {
        "date": target_date.isoformat(),
        "feast": feast,
        "lectionary": lectionary,
        "readings": readings,
    }


def display_readings(data: dict):
    """
    Pretty-print readings to console.
    """

    print(f"\n{'=' * 60}")
    print(f"  {data['date']}  |  {data['feast']}")
    print(f"  {data['lectionary']}")
    print(f"{'=' * 60}\n")

    for reading in data["readings"]:

        print(f"--- {reading['section']} ---")
        print(f"📖 {reading['reference']}")
        print()

        print(reading["text"])

        print("\n")


# ---------------- Run ---------------- #

if __name__ == "__main__":

    # Today's readings in Nairobi timezone
    data = fetch_readings()

    # Example:
    # data = fetch_readings(date(2026, 5, 18))

    display_readings(data)

    print("\nCharacter counts:\n")

    for reading in data["readings"]:
        print(
            f"{reading['section']}: "
            f"{len(reading['text'])} chars"
        )