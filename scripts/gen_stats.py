#!/usr/bin/env python3
"""Generate assets/stats.svg from the GitHub GraphQL API.

Needs GITHUB_TOKEN in the environment. Usage: python3 scripts/gen_stats.py [username]
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

USER = sys.argv[1] if len(sys.argv) > 1 else "the-BOST"
ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG, PINK, PURPLE, CYAN, TEXT = "#0d0221", "#ff2a6d", "#7b2ff7", "#00f7ff", "#d1f7ff"
FONT = "Fira Code, JetBrains Mono, Consolas, monospace"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100, isFork: false) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": USER},
    )
    data = json.load(urllib.request.urlopen(req))
    if "errors" in data:
        sys.exit(data["errors"])
    return data["data"]["user"]


def frame(w, h, title, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="neon" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{PINK}"/><stop offset="50%" stop-color="{PURPLE}"/><stop offset="100%" stop-color="{CYAN}"/>
    </linearGradient>
  </defs>
  <style>
    .t {{ font-size: 18px; font-weight: 700; fill: {PINK}; }}
    .in {{ opacity: 0; animation: in .6s ease forwards; }}
    @keyframes in {{ to {{ opacity: 1; }} }}
  </style>
  <rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="12" fill="{BG}" stroke="url(#neon)" stroke-width="3"/>
  <g fill="{TEXT}" font-family="{FONT}">
  <text class="t" x="25" y="36">{title}</text>
{body}
  </g>
</svg>
"""


def stats_card(u):
    c = u["contributionsCollection"]
    rows = [
        ("[*]", "Total stars", sum(r["stargazerCount"] for r in u["repositories"]["nodes"])),
        ("[+]", "Commits (1y)", c["totalCommitContributions"] + c["restrictedContributionsCount"]),
        ("[&gt;]", "Pull requests", c["totalPullRequestContributions"]),
        ("[!]", "Issues", c["totalIssueContributions"]),
        ("[#]", "Public repos", u["repositories"]["totalCount"]),
        ("[@]", "Followers", u["followers"]["totalCount"]),
    ]
    body = []
    for i, (icon, label, value) in enumerate(rows):
        y = 72 + i * 26
        body.append(
            f'  <g class="in" style="animation-delay:{i * 0.12:.2f}s">'
            f'<text x="25" y="{y}" font-size="14" fill="{CYAN}">{icon}</text>'
            f'<text x="62" y="{y}" font-size="14">{label}:</text>'
            f'<text x="295" y="{y}" font-size="14" font-weight="700" text-anchor="end">{value}</text></g>'
        )
    total = c["contributionCalendar"]["totalContributions"]
    body.append(
        f'  <text x="375" y="{72 + 2.5 * 26:.0f}" font-size="44" font-weight="700" text-anchor="middle" '
        f'fill="{CYAN}">{total}</text>'
        f'<text x="375" y="{100 + 2.5 * 26:.0f}" font-size="12" text-anchor="middle" opacity=".7">contributions / 1y</text>'
    )
    return frame(450, 230, f"&gt; {USER}'s stats", "\n".join(body))


if __name__ == "__main__":
    user = fetch()
    (ASSETS / "stats.svg").write_text(stats_card(user), encoding="utf-8")
    print("wrote stats.svg")
