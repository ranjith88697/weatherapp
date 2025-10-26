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
    st.info(f"Fetching weather data for **{city_name}**...")

    # 🌍 Step 1: Get coordinates using Google Geocoding API
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geo_params = {"address": city_name, "key": api_key}
    geo_response = requests.get(geo_url, params=geo_params)
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        st.warning(f"No location found for **{city_name}**. Try another name.")
        st.write("Debug info:", geo_data)
        st.stop()

    location = geo_data["results"][0]["geometry"]["location"]
    lat, lon = location["lat"], location["lng"]
    st.write(f"📍 **Latitude:** {lat}, **Longitude:** {lon}")

    # 🌤 Step 2: Fetch weather data from Google Weather API
    weather_url = "https://weather.googleapis.com/v1/currentConditions:lookup"
    weather_params = {
        "key": weather_api,
        "location.latitude": lat,
        "location.longitude": lon
    }
    weather_response = requests.get(weather_url, params=weather_params)

    if weather_response.status_code != 200:
        st.error(f"Weather API Error: {weather_response.status_code}")
        st.write(weather_response.text)
        st.stop()

    data = weather_response.json()

    # ✅ Parse and display key data (depends on Google Weather API structure)
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
