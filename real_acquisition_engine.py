cat > real_acquisition_engine.pya << 'EOF'
import os
import re
import csv
import json
import time
import random
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

STATE_DIR = "storage"
STATE_FILE = f"{STATE_DIR}/contacted_domains.json"
LEADS_FILE = "fresh_verified_leads.csv"

os.makedirs(STATE_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}

CATEGORIES = [
    "roofing",
    "hvac",
    "plumbing",
    "electrician",
    "solar",
    "med spa",
    "landscaping",
    "pest control",
    "garage door",
    "dentist"
]

CITIES = [
    "Las Vegas",
    "Phoenix",
    "Dallas",
    "Houston",
    "Miami",
    "Scottsdale",
    "Denver",
    "Austin",
    "Tampa",
    "San Diego"
]

EMAIL_REGEX = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

BAD_EMAILS = [
    "godaddy.com",
    "example.com",
    "domain.com",
    "email.com",
    "test.com"
]

BAD_WEBSITES = [
    "yelp",
    "angi",
    "facebook",
    "instagram",
    "linkedin",
    "tripadvisor",
    "yellowpages",
    "expertise",
    "bbb.org"
]

def load_contacted():

    if not os.path.exists(STATE_FILE):
        return []

    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_contacted(domains):

    with open(STATE_FILE, "w") as f:
        json.dump(domains, f, indent=2)

def clean_duckduckgo_url(url):

    if "duckduckgo.com/l/" not in url:
        return url

    parsed = urlparse(url)

    qs = parse_qs(parsed.query)

    if "uddg" in qs:
        return unquote(qs["uddg"][0])

    return url

def domain(url):

    try:
        return urlparse(url).netloc.replace("www.", "")
    except:
        return ""

def valid_website(url):

    lower = url.lower()

    for bad in BAD_WEBSITES:
        if bad in lower:
            return False

    return True

def search_businesses(query):

    url = (
        "https://duckduckgo.com/html/?q="
        + query.replace(" ", "+")
    )

    try:

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )

        results = []

        for a in soup.select("a.result__a"):

            href = a.get("href")

            if not href:
                continue

            href = clean_duckduckgo_url(href)

            if not href.startswith("http"):
                continue

            if not valid_website(href):
                continue

            results.append(href)

        return list(dict.fromkeys(results))

    except:
        return []

def scrape_business(site):

    try:

        r = requests.get(
            site,
            headers=HEADERS,
            timeout=15
        )

        html = r.text

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        title = soup.title.text.strip() if soup.title else ""

        emails = re.findall(
            EMAIL_REGEX,
            html
        )

        emails = list(set(emails))

        clean_emails = []

        for email in emails:

            bad = False

            for blocked in BAD_EMAILS:
                if blocked in email.lower():
                    bad = True

            if bad:
                continue

            clean_emails.append(email)

        if not clean_emails:
            return None

        email = clean_emails[0]

        return {
            "business": title[:120],
            "email": email,
            "website": site
        }

    except:
        return None

def main():

    contacted = load_contacted()

    verified = []

    print("\n==============================")
    print("REAL OMEGA ACQUISITION")
    print("==============================")

    for city in CITIES:

        for category in CATEGORIES:

            query = f"{category} {city}"

            print(f"\n[TARGETING] {query.upper()}")

            websites = search_businesses(query)

            print(f"[FOUND] {len(websites)} WEBSITES")

            for site in websites:

                d = domain(site)

                if not d:
                    continue

                if d in contacted:
                    print("[SKIPPED DUPLICATE]")
                    continue

                print(f"[ANALYZING] {site}")

                business = scrape_business(site)

                if not business:
                    continue

                business["category"] = category
                business["city"] = city

                verified.append(business)

                contacted.append(d)

                print(
                    f"[VERIFIED] "
                    f"{business['business']}"
                )

                time.sleep(
                    random.uniform(1.5, 3.5)
                )

                if len(verified) >= 100:
                    break

            if len(verified) >= 100:
                break

        if len(verified) >= 100:
            break

    save_contacted(contacted)

    with open(
        LEADS_FILE,
        "w",
        newline=""
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "business",
                "email",
                "website",
                "category",
                "city"
            ]
        )

        writer.writeheader()

        for row in verified:
            writer.writerow(row)

    print("\n==============================")
    print("ACQUISITION COMPLETE")
    print("==============================")

    print(f"\nVERIFIED LEADS: {len(verified)}")

    print(f"\nOUTPUT -> {LEADS_FILE}")

if __name__ == "__main__":
    main()
EOF

python real_acquisition_engine.py
