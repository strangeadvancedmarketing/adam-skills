import sys
import json
import os
import time
import urllib.request
import urllib.error
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

TIMEOUT = 10
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config", "urls.txt")

def load_urls(path):
    if not os.path.exists(path):
        return []
    urls = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls

def check_url(url):
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "UptimeCheck/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            elapsed = int((time.time() - start) * 1000)
            return {"url": url, "status": resp.status, "ms": elapsed, "ok": True}
    except urllib.error.HTTPError as e:
        elapsed = int((time.time() - start) * 1000)
        ok = e.code < 400
        return {"url": url, "status": e.code, "ms": elapsed, "ok": ok}
    except (urllib.error.URLError, socket.timeout, OSError):
        return {"url": url, "status": "TIMEOUT", "ms": None, "ok": False}

def icon(r):
    if not r["ok"]:   return "🚨"
    if isinstance(r["status"], int) and r["status"] >= 300: return "⚠️ "
    return "✅"

def render(results):
    now = datetime.now().strftime("%-m/%-d/%Y %-I:%M %p") if sys.platform != "win32" \
          else datetime.now().strftime("%#m/%#d/%Y %#I:%M %p")
    lines = [f"🌐 UPTIME CHECK — {now}", ""]

    up = sum(1 for r in results if r["ok"])
    timeouts = sum(1 for r in results if r["status"] == "TIMEOUT")
    errors = len(results) - up - timeouts

    for r in results:
        ms_str = f"({r['ms']}ms)" if r["ms"] is not None else ""
        status_str = str(r["status"])
        lines.append(f"{icon(r)}  {r['url']:<45} {status_str:<6} {ms_str}")

    lines += ["", f"{up}/{len(results)} up  |  {timeouts} timeout  |  {errors} errors"]
    return "\n".join(lines)

def main():
    args = sys.argv[1:]
    fail_only = "--fail-only" in args
    as_json   = "--json" in args
    urls_args = [a for a in args if a.startswith("http")]

    if urls_args:
        urls = urls_args
    else:
        urls = load_urls(CONFIG_FILE)
        if not urls:
            print(f"No URLs configured. Edit: {CONFIG_FILE}")
            sys.exit(1)

    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(check_url, u): u for u in urls}
        results = []
        for f in as_completed(futures):
            results.append(f.result())

    results.sort(key=lambda r: urls.index(r["url"]) if r["url"] in urls else 0)

    if fail_only:
        failures = [r for r in results if not r["ok"]]
        if not failures:
            sys.exit(0)
        for r in failures:
            ms_str = f"({r['ms']}ms)" if r["ms"] else ""
            print(f"{icon(r)}  {r['url']}  {r['status']}  {ms_str}".strip())
        sys.exit(1)

    if as_json:
        print(json.dumps(results, indent=2))
    else:
        print(render(results))

if __name__ == "__main__":
    main()
