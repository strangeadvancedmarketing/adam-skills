import urllib.request
import xml.etree.ElementTree as ET
import html
import sys
from datetime import datetime

FEEDS = {
    "general": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "tech":    "https://feeds.feedburner.com/TechCrunch",
    "business":"https://feeds.reuters.com/reuters/businessNews",
    "us":      "https://feeds.npr.org/1001/rss.xml",
    "world":   "http://feeds.bbci.co.uk/news/world/rss.xml",
}

def fetch_headlines(category="general", limit=5):
    url = FEEDS.get(category.lower(), FEEDS["general"])
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read()
    
    root = ET.fromstring(content)
    channel = root.find("channel")
    items = channel.findall("item")[:limit]
    
    today = datetime.now().strftime("%a %b %-d, %Y") if sys.platform != "win32" else datetime.now().strftime("%a %b %d, %Y").replace(" 0", " ")
    label = category.upper() if category != "general" else "TOP"
    
    output = [f"📰 {label} HEADLINES — {today}\n"]
    
    for i, item in enumerate(items, 1):
        title = html.unescape(item.findtext("title", "").strip())
        source_elem = item.find("{http://purl.org/dc/elements/1.1/}creator") or item.find("source")
        source = source_elem.text if source_elem is not None else ""
        pub_date = item.findtext("pubDate", "")
        
        # Parse relative time
        time_str = ""
        if pub_date:
            try:
                from email.utils import parsedate_to_datetime
                pub = parsedate_to_datetime(pub_date)
                delta = datetime.now(pub.tzinfo) - pub
                hours = int(delta.total_seconds() // 3600)
                if hours < 1:
                    time_str = "Just now"
                elif hours == 1:
                    time_str = "1 hour ago"
                elif hours < 24:
                    time_str = f"{hours} hours ago"
                else:
                    time_str = f"{hours // 24} days ago"
            except Exception:
                pass
        
        line = f"{i}. {title}"
        if source or time_str:
            meta = " · ".join(filter(None, [source, time_str]))
            line += f"\n   {meta}"
        output.append(line)
    
    return "\n\n".join(output)

if __name__ == "__main__":
    category = sys.argv[1] if len(sys.argv) > 1 else "general"
    try:
        print(fetch_headlines(category))
    except Exception as e:
        print(f"News unavailable: {e}")
