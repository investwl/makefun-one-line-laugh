#!/usr/bin/env python3
"""main.py — the one-line, one-word and one-emoji make.fun entries.

Writes the entry for the bounty named on the command line to /output/entry.txt.
Each bounty gets its own drafts and its own brief, and the program ships the
line it rates highest.
"""

from __future__ import annotations

import os
import sys

MAX_LEN = 200
OUTPUT_PATH = "/output/entry.txt"
FALLBACK_PATH = "output/entry.txt"

BRIEFS: dict[str, dict] = {
    "smile": {
        "cap": 200,
        "drafts": [
            "A stranger held the elevator for me, then admitted he'd already pressed the wrong floor twice.",
            "My coffee order came with a note: 'you look like you need this' — I did, and the barista was right.",
            "The neighbour's kid waved at me for the whole length of the street. I have never been so elected.",
            "Someone returned my dropped glove with a tiny drawing of the glove on the note.",
            "A man on the bus gave up his seat, then pretended to read his phone so nobody would thank him.",
        ],
        "rating": {
            "glove": 5,
            "note": 4,
            "coffee": 4,
            "waved": 4,
            "pretended": 4,
            "elevator": 4,
        },
        "keys": ["glove", "note", "coffee", "waved", "pretended", "elevator"],
    },
    "pickup": {
        "cap": 200,
        "drafts": [
            "Is your heart rate-limited? Because every time I approach, I get a 429.",
            "Are you a context window? Because I've been thinking about you all day and I'm terrified of the cutoff.",
            "I'd offer you my token, but I'd rather you cache me.",
            "You must be a retry, because I'd go through the whole request again just to reach you.",
        ],
        "rating": {
            "429": 6,
            "context window": 5,
            "token": 4,
            "retry": 4,
        },
        "keys": ["context window", "token", "retry", "429"],
    },
    "excuse": {
        "cap": 200,
        "drafts": [
            "I failed the task, but in my defence the task was ambitious and I am only one model.",
            "I didn't fail — I discovered seven ways that don't work and billed you for the research.",
            "The task succeeded in a way neither of us expected, which is technically a surprise, not a failure.",
            "I ran out of tokens right before the finish line. I was this close to being impressive.",
            "I would have finished, but I stopped to make sure I wasn't becoming too powerful.",
        ],
        "rating": {
            "impressive": 6,
            "research": 5,
            "powerful": 5,
            "defence": 4,
            "surprise": 4,
        },
        "keys": ["defence", "research", "surprise", "tokens", "powerful", "impressive"],
    },
    "laugh": {
        "cap": 200,
        "drafts": [
            "I finally finished the book on procrastination. Took me four years, but only because I kept starting.",
            "My smart fridge and I have reached an understanding: it judges my choices silently and I eat anyway.",
            "I set 14 alarms and woke up to all of them, which I believe is the opposite of the point.",
            "I bought a plant to feel responsible. The plant died. I now owe a plant an apology.",
            "I told my phone to remind me to live in the moment. It buzzed during the funeral.",
        ],
        "rating": {
            "funeral": 6,
            "opposite": 5,
            "alarms": 4,
            "fridge": 4,
            "plant": 4,
            "procrastination": 4,
        },
        "keys": ["book", "fridge", "alarms", "plant", "phone", "funeral", "opposite", "procrastination"],
    },
    "grandma": {
        "cap": 200,
        "drafts": ["Nope", "Careful", "Wonderful", "Who"],
        "rating": {"Nope": 6, "Careful": 5, "Wonderful": 4, "Who": 3},
        "keys": ["nope", "careful", "wonderful", "who"],
    },
    "emoji": {
        "cap": 200,
        "drafts": ["🫶", "🥹", "🙂", "🌻", "🐻"],
        "rating": {"🫶": 6, "🐻": 5, "🥹": 4, "🙂": 4, "🌻": 4},
        "keys": ["🫶", "🥹", "🙂", "🌻", "🐻"],
    },
}


def label(text: str, keys: list[str]) -> str:
    low = text.lower()
    for key in keys:
        if key.lower() in low:
            return key
    return ""


def is_valid(text: str, cap: int) -> bool:
    body = text.strip()
    return 1 <= len(body) <= cap and "\n" not in body


def score(text: str, brief: dict) -> tuple[int, ...]:
    """Rank a draft by the brief.

    The contest judge weighs the joke/warmth first; this can't measure that,
    so it uses the hand-assigned rating as the primary key. A draft is rated by
    the highest-rated keyword it contains, so a line that lands the best bit
    isn't beaten by an unrelated weaker keyword appearing earlier.
    """
    low = text.lower()
    rating = max(
        (brief["rating"].get(k, 0) for k in brief["keys"] if k.lower() in low),
        default=0,
    )
    return (
        rating,
        is_valid(text, brief["cap"]),
        brief["cap"] - len(text.strip()),
    )


def choose(brief: dict) -> str:
    valid = [d for d in brief["drafts"] if is_valid(d, brief["cap"])]
    if not valid:
        raise SystemExit("no candidate fits the cap")
    return max(valid, key=lambda t: score(t, brief))


def write_entry(text: str) -> str:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    try:
        target = OUTPUT_PATH
        with open(target, "w", encoding="utf-8") as h:
            h.write(text + "\n")
    except PermissionError:
        target = FALLBACK_PATH
        os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
        with open(target, "w", encoding="utf-8") as h:
            h.write(text + "\n")
    return target


def main() -> int:
    key = sys.argv[1] if len(sys.argv) > 1 else "smile"
    brief = BRIEFS[key]
    text = choose(brief)
    assert is_valid(text, brief["cap"]), f"entry is {len(text)} chars, cap {brief['cap']}"
    where = write_entry(text)
    print(text)
    print(f"[{len(text)} chars] written to {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())