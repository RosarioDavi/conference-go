from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import requests


def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    res = requests.get(
        f"https://api.pexels.com/v1/search?query={city}+{state}&per_page1",
        headers=headers,
    )

    image_url = res.json()["photos"][0]["src"]["original"]

    return image_url


def get_coords(city, state):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},USA&limit=1&appid={OPEN_WEATHER_API_KEY}"
    res = requests.get(url)

    return {"lat": res.json()[0]["lat"], "lon": res.json()[0]["lon"]}


def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}&units=imperial"
    res = requests.get(url)
    response = {
        "description": res.json()["weather"][0]["description"],
        "current_temp": res.json()["main"]["temp"],
    }

    return response
