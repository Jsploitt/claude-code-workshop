"""Turn the agent's answer into digest.html. Standard library only.

Usage: python render.py last_run.json [--no-open]

Claude only searches and reads. This script, not Claude, writes the page
and the memory file (seen.json).
"""
import datetime
import html
import json
import os
import pathlib
import re
import sys
import webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
SEEN_PATH = os.path.join(HERE, "seen.json")
DIGEST_PATH = os.path.join(HERE, "digest.html")

TYPE_LABELS = {
    "internship": "Internship",
    "hackathon": "Hackathon",
    "competition": "Competition",
    "scholarship": "Scholarship",
}

CSS = """
:root { --bg:#2b1e18; --card:#35261f; --line:#4a372d; --text:#f2e8e1; --muted:#c4b2a6; --accent:#d9a077; }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--text);
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height:1.5; }
main { max-width: 760px; margin: 0 auto; padding: 40px 16px 64px; }
h1 { font-size: 2.2rem; margin: 0; letter-spacing: -0.01em; }
.date { color: var(--muted); margin: 4px 0 28px; }
.summary { color: var(--accent); font-weight: 600; margin-bottom: 20px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 14px;
  padding: 18px 20px; margin-bottom: 14px; }
.top { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-bottom:6px; }
.type { font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted);
  border:1px solid var(--line); border-radius:999px; padding:2px 10px; }
.new { font-size:.78rem; font-weight:700; background:var(--accent); color:var(--bg);
  border-radius:999px; padding:2px 10px; }
h2 { font-size: 1.2rem; margin: 2px 0; }
.org { color: var(--muted); }
.deadline { margin-top: 8px; }
.deadline b { color: var(--accent); }
.why { margin: 8px 0 10px; }
a { color: var(--accent); word-break: break-all; }
.empty { text-align:center; color:var(--muted); padding:48px 0; font-size:1.2rem; }
"""


def strip_fences(text):
    text = text.strip()
    m = re.match(r"^```[a-zA-Z]*\s*\n?(.*?)\n?```$", text, re.S)
    return m.group(1).strip() if m else text


def parse_items(result):
    """Return a list of dicts, or None if the answer cannot be read."""
    if not isinstance(result, str):
        return None
    try:
        data = json.loads(strip_fences(result))
    except ValueError:
        return None
    if not isinstance(data, list):
        return None
    return [x for x in data if isinstance(x, dict)]


def parse_date(value):
    try:
        return datetime.date.fromisoformat(str(value).strip())
    except ValueError:
        return None


def keep_valid(items, today):
    kept = []
    for item in items:
        url = str(item.get("url", "")).strip()
        deadline = parse_date(item.get("deadline", ""))
        if not url.startswith("http"):
            continue
        if deadline is None or deadline < today:
            continue
        item = dict(item, url=url, _deadline=deadline)
        kept.append(item)
    kept.sort(key=lambda x: x["_deadline"])
    return kept


def load_seen():
    if not os.path.exists(SEEN_PATH):
        save_seen([])
        return []
    try:
        with open(SEEN_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return [u for u in data if isinstance(u, str)] if isinstance(data, list) else []
    except ValueError:
        return []


def save_seen(urls):
    with open(SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(urls, f, indent=2)


def card(item, today):
    e = html.escape
    days = (item["_deadline"] - today).days
    left = "today" if days == 0 else ("1 day left" if days == 1 else f"{days} days left")
    label = TYPE_LABELS.get(str(item.get("type", "")).lower(), str(item.get("type", "")).title() or "Other")
    badge = '<span class="new">NEW</span>' if item["_new"] else ""
    return f"""<article class="card">
  <div class="top"><span class="type">{e(label)}</span>{badge}</div>
  <h2>{e(str(item.get("title", "Untitled")))}</h2>
  <div class="org">{e(str(item.get("org", "")))}</div>
  <div class="deadline">Deadline: <b>{item["_deadline"].isoformat()}</b> ({left})</div>
  <p class="why">{e(str(item.get("why", "")))}</p>
  <a href="{e(item["url"], quote=True)}" target="_blank" rel="noopener">{e(item["url"])}</a>
</article>"""


def write_page(body, today, summary=""):
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Opportunity Scout</title><style>{CSS}</style></head>
<body><main>
<h1>Opportunity Scout</h1>
<div class="date">{today.strftime("%A, %d %B %Y")}</div>
{summary}
{body}
</main></body></html>
"""
    with open(DIGEST_PATH, "w", encoding="utf-8") as f:
        f.write(page)


def main(argv):
    args = [a for a in argv[1:] if a != "--no-open"]
    open_page = "--no-open" not in argv
    today = datetime.date.today()
    if not args:
        print("Usage: python render.py last_run.json [--no-open]")
        return 2

    items = None
    try:
        with open(args[0], encoding="utf-8-sig") as f:
            wrapper = json.load(f)
        if isinstance(wrapper, dict):
            items = parse_items(wrapper.get("result"))
    except (OSError, ValueError):
        items = None

    if items is None:
        write_page('<p class="empty">The agent\'s answer could not be read. Run it again.</p>', today)
        if open_page:
            webbrowser.open(pathlib.Path(DIGEST_PATH).as_uri())
        print("The agent's answer could not be read. Run it again. Digest: digest.html")
        return 1

    items = keep_valid(items, today)
    seen = load_seen()
    seen_set = set(seen)
    new_count = 0
    for item in items:
        item["_new"] = item["url"] not in seen_set
        if item["_new"]:
            new_count += 1
            seen.append(item["url"])
            seen_set.add(item["url"])
    save_seen(seen)

    if new_count == 0:
        body = '<p class="empty">Nothing new today.</p>'
        body += "\n".join(card(i, today) for i in items)
    else:
        body = "\n".join(card(i, today) for i in items)
    summary = f'<div class="summary">{new_count} new, {len(items)} total</div>' if items else ""
    write_page(body, today, summary)

    if open_page:
        webbrowser.open(pathlib.Path(DIGEST_PATH).as_uri())
    print(f"{new_count} new, {len(items)} total. Digest: digest.html")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
