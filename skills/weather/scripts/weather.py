import urllib.request
import json
import sys

def get_weather(city):
    city_enc = urllib.parse.quote(city)
    url = f"https://wttr.in/{city_enc}?format=j1"
    
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.68.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    current = data["current_condition"][0]
    today = data["weather"][0]
    tomorrow = data["weather"][1] if len(data["weather"]) > 1 else None
    area = data["nearest_area"][0]
    
    area_name = area["areaName"][0]["value"]
    country = area["country"][0]["value"]
    
    temp_f = current["temp_F"]
    feels_f = current["FeelsLikeF"]
    humidity = current["humidity"]
    wind_mph = current["windspeedMiles"]
    wind_dir = current["winddir16Point"]
    desc = current["weatherDesc"][0]["value"]
    
    max_f = today["maxtempF"]
    min_f = today["mintempF"]
    
    hourly = today.get("hourly", [])
    evening_desc = ""
    for h in hourly:
        if int(h["time"]) >= 2000:
            evening_desc = h["weatherDesc"][0]["value"]
            break
    
    output = f"{area_name}, {country} — {temp_f}°F, {desc}\n"
    output += f"Feels like {feels_f}°F | Humidity {humidity}% | Wind {wind_mph} mph {wind_dir}\n"
    output += f"Today: High {max_f}°F / Low {min_f}°F\n"
    if evening_desc:
        output += f"Tonight: {evening_desc}\n"
    if tomorrow:
        t_max = tomorrow["maxtempF"]
        t_desc = tomorrow["hourly"][4]["weatherDesc"][0]["value"] if tomorrow.get("hourly") else ""
        output += f"Tomorrow: {t_desc}, High {t_max}°F\n"
    
    return output.strip()

if __name__ == "__main__":
    import urllib.parse
    city = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Miami, FL"
    try:
        print(get_weather(city))
    except Exception as e:
        print(f"Weather unavailable: {e}")
