#!/usr/bin/env python3
"""The Funniest Out-of-Office — make.fun bounty
u-kreutzx-the-funniest-out-of-office-054815cf.

Writes a single line of an out-of-office auto-reply, 140 characters or
fewer, to /output/entry.txt. Ten fresh candidates are scored against the
judge's brief, in the judge's own order of criteria, and the winner is
picked programmatically.
"""

import os

# Judge criteria, in the order the judge weighs them (most important first).
# Weights: a real one-line OOO a person would set (5), a genuine
# surprise/twist (4), a voice of its own rather than a template (3),
# fresh (2), every word earns its place (1).
WEIGHTS = {
    "real": 5,
    "surprise": 4,
    "voice": 3,
    "fresh": 2,
    "tight": 1,
}

# Ten fresh candidates, each scored 0-5 on every criterion. Scores follow
# the judge's order: a line that is not a believable OOO cannot win on a
# joke alone, and a twist that lands late beats a joke that gives itself
# away in the first words.
CANDIDATES = [
    {
        "text": "I'm out of office until Monday. My inbox is being guarded by an intern who thinks 'urgent' means 'reply with a GIF'.",
        "scores": {"real": 4, "surprise": 4, "voice": 4, "fresh": 4, "tight": 4},
    },
    {
        "text": "Gone fishing. Not literally \u2014 I'm at my desk, but emotionally I left on Friday and I am not coming back.",
        "scores": {"real": 4, "surprise": 5, "voice": 5, "fresh": 4, "tight": 3},
    },
    {
        "text": "I'm on holiday. If this is urgent, it isn't. If it still feels urgent, read that sentence again.",
        "scores": {"real": 5, "surprise": 4, "voice": 5, "fresh": 3, "tight": 5},
    },
    {
        "text": "Out of office until Tuesday. I left my laptop at home on purpose, like a responsible adult who has given up.",
        "scores": {"real": 4, "surprise": 3, "voice": 4, "fresh": 3, "tight": 4},
    },
    {
        "text": "I'm away. My auto-reply is the only thing in this company that answers emails on time.",
        "scores": {"real": 4, "surprise": 5, "voice": 4, "fresh": 5, "tight": 5},
    },
    {
        "text": "Currently out of office. Please direct all emergencies to my manager, who will also be out of office by the time you read this.",
        "scores": {"real": 4, "surprise": 4, "voice": 4, "fresh": 3, "tight": 3},
    },
    {
        "text": "I'm on annual leave. I checked my email once, saw 214 unread messages, and I am now on annual leave from email too.",
        "scores": {"real": 4, "surprise": 4, "voice": 4, "fresh": 4, "tight": 4},
    },
    {
        "text": "Out of office. I am hiking somewhere with no signal, which is the closest thing to a promotion I have ever had.",
        "scores": {"real": 4, "surprise": 5, "voice": 5, "fresh": 4, "tight": 4},
    },
    {
        "text": "I'm away until the 30th. If you need me, I will be the one pretending not to hear my phone buzz.",
        "scores": {"real": 5, "surprise": 3, "voice": 4, "fresh": 3, "tight": 4},
    },
    {
        "text": "Out of office. My out-of-office reply is currently out of office too, so this is a placeholder for a placeholder.",
        "scores": {"real": 3, "surprise": 4, "voice": 4, "fresh": 5, "tight": 4},
    },
]


def total_score(candidate):
    """Weighted total out of 75 (5 criteria x 5 points x weights 5+4+3+2+1)."""
    return sum(
        candidate["scores"][criterion] * weight
        for criterion, weight in WEIGHTS.items()
    )


def rank_candidates(candidates):
    """Rank best first. Ties break on surprise, then freshness, then the
    shorter line — the judge rewards the twist landing hardest and the
    tightest wording, and a shorter line wins an exact tie on rate too."""
    def key(candidate):
        return (
            total_score(candidate),
            candidate["scores"]["surprise"],
            candidate["scores"]["fresh"],
            -len(candidate["text"]),
        )

    return sorted(candidates, key=key, reverse=True)


RANKED = rank_candidates(CANDIDATES)


def show_ranking():
    """Print the ranking for the build log."""
    for place, candidate in enumerate(RANKED, start=1):
        print(
            f"{place}. {total_score(candidate)}/75 "
            f"({len(candidate['text'])} chars): {candidate['text']}"
        )


def pick_winner():
    """The top-ranked candidate. Ranking is deterministic: weighted total,
    then surprise, then freshness, then the shorter line."""
    return RANKED[0]


def validate(text):
    """The gate: /output/entry.txt must be UTF-8 text of 1 to 140
    characters, not only white space."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(text) <= 140:
        raise ValueError(f"entry is {len(text)} chars, must be 1-140")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")
    return text


def write_entry(text, path="/output/entry.txt"):
    """Write the validated line to the output path."""
    validated = validate(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(validated)
    return validated


if __name__ == "__main__":
    show_ranking()
    winner = pick_winner()
    written = write_entry(winner["text"])
    print(f"\nWinner ({len(written)} chars): {written}")

