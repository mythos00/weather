from fastapi import FastAPI, HTTPException
import urllib.request
import urllib.parse
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# HAVA MƏLUMATINI AL
# =========================

@app.get("/weather")
def get_weather(city: str):

    try:
        # =========================
        # ŞƏHƏRİN KOORDİNATLARINI TAP
        # =========================

        params = urllib.parse.urlencode({
            "name": city,
            "count": 1,
            "language": "az",
            "format": "json"
        })

        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            + params
        )

        with urllib.request.urlopen(
            geo_url,
            timeout=10
        ) as response:

            geo_data = json.loads(
                response.read().decode("utf-8")
            )

        if "results" not in geo_data:
            raise HTTPException(
                status_code=404,
                detail="Bu şəhər tapılmadı."
            )

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]


        # =========================
        # HAVA MƏLUMATLARINI AL
        # =========================

        weather_params = urllib.parse.urlencode({
            "latitude": latitude,
            "longitude": longitude,

            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "weather_code,"
                "wind_speed_10m"
            ),

            "timezone": "auto"
        })

        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            + weather_params
        )

        with urllib.request.urlopen(
            weather_url,
            timeout=10
        ) as response:

            weather_data = json.loads(
                response.read().decode("utf-8")
            )


        # =========================
        # CURRENT MƏLUMATLARI
        # =========================

        current = weather_data["current"]

        temperature = current["temperature_2m"]
        feels_like = current["apparent_temperature"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]
        weather_code = current["weather_code"]


        # =========================
        # HAVA VƏZİYYƏTLƏRİ
        # =========================

        conditions = {

            0: ("☀️", "Açıq hava"),

            1: ("🌤️", "Əsasən açıq"),

            2: ("⛅", "Qismən buludlu"),

            3: ("☁️", "Buludlu"),

            45: ("🌫️", "Dumanlı"),

            48: ("🌫️", "Dumanlı"),

            51: ("🌦️", "Yüngül çiskin"),

            53: ("🌦️", "Çiskin"),

            55: ("🌧️", "Güclü çiskin"),

            61: ("🌧️", "Yüngül yağış"),

            63: ("🌧️", "Yağış"),

            65: ("🌧️", "Güclü yağış"),

            71: ("🌨️", "Yüngül qar"),

            73: ("❄️", "Qar"),

            75: ("❄️", "Güclü qar"),

            80: ("🌧️", "Yağış"),

            81: ("🌧️", "Yağış"),

            82: ("🌧️", "Güclü yağış"),

            95: ("⛈️", "Tufan"),

            96: ("⛈️", "Tufan və dolu"),

            99: ("⛈️", "Güclü tufan")
        }


        icon, condition = conditions.get(
            weather_code,
            ("🌡️", "Naməlum")
        )


        # =========================
        # NƏTİCƏ
        # =========================

        now = datetime.now()

        return {

            "city": location["name"],

            "country": location.get(
                "country",
                ""
            ),

            "date": now.strftime(
                "%d.%m.%Y"
            ),

            "time": now.strftime(
                "%H:%M"
            ),

            "temperature": round(
                temperature
            ),

            "feels_like": round(
                feels_like
            ),

            "humidity": humidity,

            "wind": wind,

            "weather_code": weather_code,

            "icon": icon,

            "condition": condition
        }


    except HTTPException:
        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Hava məlumatını almaq mümkün olmadı: {error}"
        )