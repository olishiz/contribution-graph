#!/usr/bin/env python3
"""Roll 1–5 empty commits for each Kuala Lumpur day that does not have one yet.

GitHub places a commit on the calendar day stored in the author timestamp,
including the UTC offset. Stamping noon in Asia/Kuala_Lumpur keeps the square
on that Kuala Lumpur date. A second run on the same KL day does nothing.
"""

from __future__ import annotations

import argparse
import os
import random
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

KL = ZoneInfo("Asia/Kuala_Lumpur")
DEFAULT_EMAIL = "zhuen1101@hotmail.com"
DEFAULT_NAME = "olishiz"
MIN_COMMITS = 1
MAX_COMMITS = 5
MAX_DAYS = 366


@dataclass(frozen=True)
class DayPlan:
    day: date
    commits: int

    def stamps(self) -> list[str]:
        return [
            datetime(self.day.year, self.day.month, self.day.day, 12, minute, 0, tzinfo=KL).strftime(
                "%Y-%m-%dT%H:%M:%S%z"
            )
            for minute in range(self.commits)
        ]


def kl_day(moment: datetime) -> date:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=KL)
    return moment.astimezone(KL).date()


def parse_instant(value: str) -> datetime:
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def occupied_days(author_instants: list[str]) -> set[date]:
    return {kl_day(parse_instant(value)) for value in author_instants if value.strip()}


def plan(today: date, occupied: set[date], days: int, rng: random.Random) -> list[DayPlan]:
    if days < 1:
        raise SystemExit("days must be at least 1.")
    if days > MAX_DAYS:
        raise SystemExit(f"days must be {MAX_DAYS} or fewer. The graph shows about a year.")
    chosen: list[DayPlan] = []
    for offset in range(days):
        day = today - timedelta(days=offset)
        if day in occupied:
            continue
        chosen.append(DayPlan(day, rng.randint(MIN_COMMITS, MAX_COMMITS)))
    chosen.sort(key=lambda item: item.day)
    return chosen


def author_instants(repo: str) -> list[str]:
    result = subprocess.run(
        ["git", "log", "--format=%aI"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def commit_days(repo: str, plans: list[DayPlan], name: str, email: str) -> int:
    made = 0
    for item in plans:
        for stamp in item.stamps():
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = stamp
            env["GIT_COMMITTER_DATE"] = stamp
            subprocess.run(
                [
                    "git",
                    "-c",
                    f"user.name={name}",
                    "-c",
                    f"user.email={email}",
                    "commit",
                    "--allow-empty",
                    "-m",
                    f"chore: contribution {item.day.isoformat()} [skip ci]",
                ],
                cwd=repo,
                env=env,
                check=True,
            )
            made += 1
    return made


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Commit 1–5 times per open Kuala Lumpur day.")
    parser.add_argument("--repo", default=".")
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--email", default=os.environ.get("GIT_EMAIL") or DEFAULT_EMAIL)
    parser.add_argument("--name", default=os.environ.get("GIT_NAME") or DEFAULT_NAME)
    parser.add_argument("--now", default=None, help="ISO-8601 timestamp to treat as the current time.")
    args = parser.parse_args(argv)

    raw_days = args.days
    if raw_days is None:
        raw_days = int((os.environ.get("MAX_DAYS") or "1").strip() or "1")
    moment = parse_instant(args.now) if args.now else datetime.now(KL)
    today = kl_day(moment)
    plans = plan(today, occupied_days(author_instants(args.repo)), raw_days, random.SystemRandom())
    made = commit_days(args.repo, plans, args.name, args.email) if plans else 0

    print(f"kl_day={today.isoformat()}")
    print(f"days={len(plans)}")
    print(f"commits={made}")
    print(f"reason={'recorded' if made else 'already-recorded'}")
    if plans:
        print("filled " + ", ".join(item.day.isoformat() for item in plans), file=sys.stderr)
    else:
        print(f"already recorded {today.isoformat()} in Kuala Lumpur", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
