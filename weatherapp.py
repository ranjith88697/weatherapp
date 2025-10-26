import streamlit as st
import requests

st.title("🌦 Weather App with Google APIs")

# ✅ Make sure these secrets exist in .streamlit/secrets.toml
#api_key = st.secrets["GOOGLE_API_KEY"]
#weather_api = st.secrets["G_WEATHER_API"]
api_key = "AIzaSyAX3v9OSj4Fg3Ad649BIRR13B09CidYNqc"
weather_api = "AIzaSyBF5T-bQzl9-NFJ_aHMzTgTntqC-TjMIw4"

# ✅ Input for user
city_name = st.text_input("Enter your city:", "Riga")

if st.button("Get Weather"):
    #st.write("Loaded keys:", "GOOGLE_API_KEY" in st.secrets, "G_WEATHER_API" in st.secrets)
    # ✅ 1️⃣ Get latitude & longitude using Geocoding API
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geo_params = {"address": city_name, "key": api_key}
    geo_response = requests.get(geo_url, params=geo_params)
    geo_data = geo_response.json()

    if geo_data.get("results"):
        location = geo_data["results"][0]["geometry"]["location"]
        lat, lon = location["lat"], location["lng"]

        # ✅ 2️⃣ Get weather using Google Weather API
        weather_url = "https://weather.googleapis.com/v1/currentConditions:lookup"
        weather_params = {
            "key": weather_api,
            "location.latitude": lat,
            "location.longitude": lon
        }
        weather_response = requests.get(weather_url, params=weather_params)

        # ✅ 3️⃣ Display result
    if weather_response.status_code != 200:
        st.error(f"Weather API Error: {weather_response.status_code}")
        st.write(weather_response.text)
        st.stop()

        data = weather_response.json()
    
    else:
        st.warning(f"No results found for '{city_name}'. Try another city name.")
        st.write("Full API response:", geo_data)

        st.subheader(f"🌍 Current Weather in {city_name.title()}")

    try:
        conditions = data.get("currentConditions", {})
        temp = conditions.get("temperature", {}).get("value", "N/A")
        humidity = conditions.get("humidity", {}).get("value", "N/A")
        wind_speed = conditions.get("windSpeed", {}).get("value", "N/A")
        condition_desc = conditions.get("conditionDescription", "N/A")

        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperature", f"{temp}°C")
        col2.metric("💧 Humidity", f"{humidity}%")
        col3.metric("🌬️ Wind Speed", f"{wind_speed} m/s")

        st.write(f"**Condition:** {condition_desc}")
        st.divider()
        st.caption("📘 Data provided by Google Weather API")

    except Exception as e:
        st.error("Unable to parse weather data — see raw response below:")
        st.json(data)
