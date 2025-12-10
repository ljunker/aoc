from __future__ import annotations

import os
import re
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Optional

import requests


AOC_BASE_URL = "https://adventofcode.com"


class SubmissionStatus(Enum):
    CORRECT = auto()
    INCORRECT = auto()
    TOO_RECENT = auto()
    ALREADY_COMPLETED = auto()
    UNKNOWN = auto()


@dataclass
class SubmissionResult:
    status: SubmissionStatus
    message: str
    raw_html: str


@dataclass
class AdventOfCodeClient:
    """
    Small helper client for Advent of Code.

    - Uses a session cookie (from your browser).
    - Caches puzzle input locally.
    - Can submit answers and parse basic feedback.
    """

    session_token: Optional[str] = None
    cache_dir: Path = Path(".aoc_cache")
    user_agent: str = "AdventOfCodeHelper (github.com/yourname/yourrepo)"
    base_url: str = AOC_BASE_URL

    def __post_init__(self) -> None:
        if self.session_token is None:
            self.session_token = os.environ.get("AOC_SESSION")

        if not self.session_token:
            raise ValueError(
                "No AoC session token provided. "
                "Set AOC_SESSION env var or pass session_token=..."
            )

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.user_agent,
            }
        )
        self.session.cookies.set("session", self.session_token)

        self.cache_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------
    # Helpers
    # ---------------------------

    def _input_cache_path(self, year: int, day: int) -> Path:
        year_dir = self.cache_dir / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        return year_dir / f"day{day:02d}.txt"

    def _puzzle_url(self, year: int, day: int) -> str:
        return f"{self.base_url}/{year}/day/{day}"

    def _input_url(self, year: int, day: int) -> str:
        return f"{self._puzzle_url(year, day)}/input"

    def _answer_url(self, year: int, day: int) -> str:
        return f"{self._puzzle_url(year, day)}/answer"

    # ---------------------------
    # Public API
    # ---------------------------

    def get_input(self, year: int, day: int, force: bool = False) -> str:
        """
        Get puzzle input for given year/day.
        Caches it under cache_dir/year/dayXX.txt.
        """

        cache_path = self._input_cache_path(year, day)

        if cache_path.exists() and not force:
            return cache_path.read_text(encoding="utf-8")

        url = self._input_url(year, day)
        resp = self.session.get(url)
        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to fetch input (HTTP {resp.status_code}). "
                "Check your session cookie and that the puzzle is unlocked."
            )

        text = resp.text.rstrip("\n")
        cache_path.write_text(text, encoding="utf-8")
        return text

    def submit_answer(
        self,
        year: int,
        day: int,
        level: int,
        answer: str,
    ) -> SubmissionResult:
        """
        Submit an answer for a specific part (level 1 or 2).

        Returns a SubmissionResult with status + message.
        """

        url = self._answer_url(year, day)
        data = {
            "level": str(level),
            "answer": str(answer).strip(),
        }

        resp = self.session.post(url, data=data)
        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to submit answer (HTTP {resp.status_code})."
            )

        html = resp.text
        status, msg = self._parse_submission_response(html)

        return SubmissionResult(status=status, message=msg, raw_html=html)

    def get_leaderboard(self, year, board_id):
        url = f"{self.base_url}/{year}/leaderboard/private/view/{board_id}.json"
        resp = self.session.get(url)
        if resp.status_code != 200:
            raise RuntimeError(
                f"Failed to get leaderboard (HTTP {resp.status_code})."
            )
        return resp.json()

    # ---------------------------
    # Parsing
    # ---------------------------

    @staticmethod
    def _parse_submission_response(html: str) -> tuple[SubmissionStatus, str]:
        """
        Naive HTML parsing to map AoC's response messages to a status.
        """

        # Keep it super simple: look inside the <article> content
        match = re.search(r"<article[^>]*>(.*?)</article>", html, re.DOTALL | re.IGNORECASE)
        if match:
            text = re.sub(r"<.*?>", "", match.group(1))  # strip tags
            text = " ".join(text.split())  # normalize whitespace
        else:
            text = html

        text_lower = text.lower()

        if "that's the right answer" in text_lower:
            return SubmissionStatus.CORRECT, text
        if "that's not the right answer" in text_lower:
            return SubmissionStatus.INCORRECT, text
        if "you gave an answer too recently" in text_lower:
            return SubmissionStatus.TOO_RECENT, text
        if "you don't seem to be solving the right level" in text_lower:
            return SubmissionStatus.ALREADY_COMPLETED, text

        return SubmissionStatus.UNKNOWN, text
