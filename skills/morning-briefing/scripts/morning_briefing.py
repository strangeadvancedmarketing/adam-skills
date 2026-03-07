import sys
import os
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable

def run_weather(city):
    weather_script = os.path.join(SCRIPT_DIR, "..", "..", "weather", "scripts", "weather.py")
    weather_script = os.path.normpath(weather_script)
    try:
        result = subprocess.run([PYTHON, weather_script, city], capture_output=True, text=True, timeout=15)
        return result.stdout.strip() if result.returncode == 0 else f"Weather unavailable"
    except Exception as e:
        return f"Weather unavailable: {e}"

def run_news(category="general", limit=5):
    news_script = os.path.join(SCRIPT_DIR, "..", "..", "news-headlines", "scripts", "news.py")
    news_script = os.path.normpath(news_script)
    try:
        result = subprocess.run([PYTHON, news_script, category], capture_output=True, text=True, timeout=15)
        return result.stdout.strip() if result.returncode == 0 else "News unavailable"
    except Exception as e:
        return f"News unavailable: {e}"

def format_briefing(city, weather, news, email_section=None):
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    lines = [
        f"☀️  MORNING BRIEFING — {today}",
        "",
        "WEATHER",
        weather,
        "",
        news,
    ]
    
    if email_section:
        lines += ["", "EMAIL", email_section]
    
    return "\n".join(lines)

if __name__ == "__main__":
    city = sys.argv[1] if len(sys.argv) > 1 else "Miami, FL"
    include_email = "--email" in sys.argv
    
    weather = run_weather(city)
    news = run_news()
    
    email_section = None
    if include_email:
        email_section = "Configure email plugin to see unread count here."
    
    print(format_briefing(city, weather, news, email_section))
