#!/usr/bin/env python3
import colorsys
import os
import re
import sys
from functools import reduce

import requests
from bs4 import BeautifulSoup

AOC_EVENTS_URL = "https://adventofcode.com/events"
SESSION_ENV_VAR = "AOC_SESSION"


def get_session_cookie() -> str:
    session = os.getenv(SESSION_ENV_VAR)
    if not session:
        print(f"Error: environment variable {SESSION_ENV_VAR} is not set.", file=sys.stderr)
        print("Export your AoC session token, e.g.:", file=sys.stderr)
        print(f'  export {SESSION_ENV_VAR}="…your session cookie…"')
        sys.exit(1)
    return session


def fetch_events_html(session_cookie: str) -> str:
    headers = {
        "Cookie": f"session={session_cookie}",
        "User-Agent": "aoc-events-parser (https://adventofcode.com/)",
    }
    resp = requests.get(AOC_EVENTS_URL, headers=headers)
    resp.raise_for_status()
    return resp.text


def parse_events(html: str):
    soup = BeautifulSoup(html, "html.parser")

    stars_per_year = {}

    # Each year row: <div class="eventlist-event"> ... </div>
    for div in soup.select("div.eventlist-event"):
        link = div.find("a")
        if not link:
            continue

        # Link text is like "[2025]"
        m = re.search(r"\[(\d{4})]", link.get_text())
        if not m:
            # Sometimes the current year link is just "/" with "[2025]" text
            # but the regex above should catch it; still, be defensive.
            continue

        year = int(m.group(1))

        # First span.star-count inside the div is your stars for that year
        stars_span = div.find("span", class_="star-count")
        if stars_span is not None:
            stars_text = stars_span.get_text(strip=True)
            # e.g. "18*"
            stars = int(stars_text.rstrip("*").strip())
        else:
            # years you never started show no span at all
            stars = 0

        stars_per_year[year] = stars

    # Parse "Total stars" line
    total_stars = None
    for p in soup.find_all("p"):
        if "Total stars" in p.get_text():
            total_span = p.find("span", class_="star-count")
            if total_span:
                total_text = total_span.get_text(strip=True)
                total_stars = int(total_text.rstrip("*").strip())
            break

    return stars_per_year, total_stars

STAR = "⭐"

def fmt_year_badge(year: int, stars: int, color: str) -> str:
    return f"https://img.shields.io/badge/{year}-{stars}%20{STAR}-{color}?style=flat-square"


def fmt_total_badge(stars: int, color: str) -> str:
    return f"https://img.shields.io/badge/total-{stars}%20{STAR}-{color}?style=for-the-badge"

def rgb2hex(r, g, b):
    f = lambda x: max(0, min(255, round(x * 255)))
    return f"{f(r):02x}{f(g):02x}{f(b):02x}"


def hsv_interp(t):
    # 0 - 60 - 120
    assert 0 <= t <= 1
    return rgb2hex(*colorsys.hsv_to_rgb(h=t * 120 / 360, s=1, v=0.6))


def get_year_badge_url(year: int, stars: int) -> str:
    total_stars = 50 if year < 2025 else 24
    color = hsv_interp(stars / total_stars)

    badge = f'<img src="{fmt_year_badge(year, stars, color)}"></img>'

    return badge


def get_total_badge_url(stars: int, years: list) -> str:
    color = hsv_interp(stars / reduce(lambda x, y: x + y, [50 if y < 2025 else 24 for y in years]))
    return f'<a href="./README.md"><img src="{fmt_total_badge(stars, color)}"></img></a>'


def main():
    session_cookie = get_session_cookie()
    html = fetch_events_html(session_cookie)
    stars_per_year, total_stars = parse_events(html)

    # Print sorted by year descending (most recent first)
    for year in sorted(stars_per_year.keys(), reverse=True):
        stars = stars_per_year[year]
        print(get_year_badge_url(year, stars))

    if total_stars is not None:
        print("-" * 20)
        print(get_total_badge_url(total_stars, [year for year in sorted(stars_per_year.keys(), reverse=True)]))


if __name__ == "__main__":
    main()
