import streamlit as st
import requests
from datetime import datetime
import pytz
import json

st.title("🌦 Weather App with Google APIs")

#api_key = st.secrets["GOOGLE_API_KEY"]
#weather_api = st.secrets["G_WEATHER_API"]
api_key = "AIzaSyAX3v9OSj4Fg3Ad649BIRR13B09CidYNqc"
weather_api = "AIzaSyBF5T-bQzl9-NFJ_aHMzTgTntqC-TjMIw4"

#Input for user
city_name = st.text_input("Enter your city:", "Riga")

if st.button("Get Weather"):
    st.info(f"Fetching weather data for **{city_name}**...")

    #Step 1: Get coordinates using Google Geocoding API
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

    #Step 2: Fetch weather data from Google Weather API
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
    #st.write("DEBUG: raw weather JSON:") -- for Debugging
    #st.json(data) -- for Debugging
    #Parse and display key data (depends on Google Weather API structure)
    st.subheader(f"🌍 Current Weather in {city_name.title()}")

def safe(d, *keys, default=None):
    """Safe nested dict getter: safe(data, 'a','b') -> data['a']['b'] or default"""
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d

def display_weather(data, city_name="city_name"):
    # Basic fields
    current_time = safe(data, "currentTime")
    timezone_id = safe(data, "timeZone", "id", default="UTC")
    is_day = safe(data, "isDaytime", default=None)

    cond_text = safe(data, "weatherCondition", "description", "text", default="N/A")
    icon_base = safe(data, "weatherCondition", "iconBaseUri", default=None)
    condition_type = safe(data, "weatherCondition", "type", default=None)

    temp = safe(data, "temperature", "degrees", default="N/A")
    temp_unit = safe(data, "temperature", "unit", default="CELSIUS")

    feels_like = safe(data, "feelsLikeTemperature", "degrees", default="N/A")
    humidity = safe(data, "relativeHumidity", default="N/A")
    dew_point = safe(data, "dewPoint", "degrees", default="N/A")
    wind_speed = safe(data, "wind", "speed", "value", default="N/A")
    wind_unit = safe(data, "wind", "speed", "unit", default=None)
    wind_dir = safe(data, "wind", "direction", "cardinal", default="N/A")
    wind_gust = safe(data, "wind", "gust", "value", default=None)
    visibility = safe(data, "visibility", "distance", default="N/A")
    visibility_unit = safe(data, "visibility", "unit", default=None)
    pressure = safe(data, "airPressure", "meanSeaLevelMillibars", default="N/A")
    uv = safe(data, "uvIndex", default="N/A")
    precip_prob = safe(data, "precipitation", "probability", "percent", default="N/A")
    precip_qpf = safe(data, "precipitation", "qpf", "quantity", default="N/A")
    precip_unit = safe(data, "precipitation", "qpf", "unit", default=None)
    cloud_cover = safe(data, "cloudCover", default="N/A")

    # History / min/max
    temp_min = safe(data, "currentConditionsHistory", "minTemperature", "degrees", default=None)
    temp_max = safe(data, "currentConditionsHistory", "maxTemperature", "degrees", default=None)
    qpf_history = safe(data, "currentConditionsHistory", "qpf", "quantity", default=None)

    # time with timezone 
    if current_time:
        try:
            dt = datetime.fromisoformat(current_time.replace("Z", "+00:00"))
            try:
                tz = pytz.timezone(timezone_id)
                dt_local = dt.astimezone(tz)
                st.caption(f"Updated: {dt_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            except Exception:
                st.caption(f"Updated (UTC): {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        except Exception:
            st.caption(f"Time: {current_time}")

    # Top row: icon + main temperature & condition
    col_icon, col_main = st.columns([1, 4])
    with col_icon:
        if icon_base:
            # iconBaseUri may be a base path — try to show it (some providers append names)
            st.image(icon_base, width=72)
    with col_main:
        st.markdown(f"### {temp}° {temp_unit.capitalize()}  —  **{cond_text}**")
        if condition_type:
            st.write(f"*Condition type:* `{condition_type}`")
        st.write(f"Feels like: **{feels_like}° {temp_unit.capitalize()}**")

    st.write("---")

    # Key metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("💧 Humidity", f"{humidity}%")
    m2.metric("🌬️ Wind", f"{wind_speed} {wind_unit or ''}", delta=f"{wind_dir}")
    m3.metric("🔆 UV Index", f"{uv}")

    # Secondary row
    s1, s2, s3 = st.columns(3)
    s1.write(f"**Dew point:** {dew_point}° {temp_unit.capitalize()}")
    s2.write(f"**Pressure (MSL):** {pressure} mb")
    s3.write(f"**Visibility:** {visibility} {visibility_unit or ''}")

    # Precipitation & cloud
    st.write(f"**Precipitation probability:** {precip_prob}%")
    st.write(f"**Precipitation (QPF):** {precip_qpf} {precip_unit or ''}")
    st.write(f"**Cloud cover:** {cloud_cover}%")

    # Wind gust if exists
    if wind_gust:
        st.write(f"**Wind gust:** {wind_gust} {wind_unit or ''}")

    # History / min-max
    if temp_max is not None or temp_min is not None or qpf_history is not None:
        st.write("---")
        st.write("**History / Summary**")
        if temp_max is not None:
            st.write(f"- Max temp: {temp_max}° {temp_unit}")
        if temp_min is not None:
            st.write(f"- Min temp: {temp_min}° {temp_unit}")
        if qpf_history is not None:
            st.write(f"- Total QPF (history): {qpf_history} mm")

    st.caption("Data source: Google Weather API (parsed)")
display_weather(data, city_name=city_name)
# Example usage:
# display_weather(data, city_name="Riga")
