import streamlit as st
import requests
#from google.colab import userdata
#Get Lat and Lng based on city, country
#api_key = userdata.get('GOOGLE_API_KEY') # Get the API key from userdata
st.title("🌦 Weather App with Google APIs")
api_key = st.secrets["GOOGLE_API_KEY"]
#weather_api = userdata.get('G_WEATHER_API')
weather_api = st.secrets["G_WEATHER_API"]
city_name = st.text_input("Enter your city:", "Riga" )
address = city_name
#url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"

if st.button("Get Weather"):
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geo_params = {"address": address, "key": api_key}

    geo_response = requests.get(geo_url, params=geo_params)
    geo_data = geo_response.json()

    # ✅ Check for valid results
    if geo_data.get("results"):
        location = geo_data["results"][0]["geometry"]["location"]
        lat, lon = location["lat"], location["lng"]

        weather_url = "https://weather.googleapis.com/v1/currentConditions:lookup"
        weather_params = {
            "key": weather_api,
            "location.latitude": lat,
            "location.longitude": lon
        }
        weather_response = requests.get(weather_url, params=weather_params)

        if weather_response.status_code == 200:
            st.json(weather_response.json())
        else:
            st.error(f"Weather API error: {weather_response.status_code}")
    else:
        st.warning(f"No results found for '{place}'. Try another name.")
        st.write("Full API response:", geo_data)

'''
url = "https://maps.googleapis.com/maps/api/geocode/json"
geo_param = {"address" : adddress, "key" : api_key}
geo_response = requests.get(url, params=geo_param)
location = geo_response.json()['results'][0]['geometry']['location']
Latitude =  float(location['lat'])
Longitude =  float(location['lng'])
print(round(Latitude,2))
print(round(Longitude,2))
print(f"Latitude: {location['lat']}, Longitude: {location['lng']}")

url_weather = "https://weather.googleapis.com/v1/currentConditions:lookup"

params = {
    "key": weather_api,
    "location.latitude": Latitude,
    "location.longitude": Longitude
}

response = requests.get(url_weather, params=params)

#base_url = 'https://weather.googleapis.com/v1/currentConditions:lookup?key=AIzaSyBF5T-bQzl9-NFJ_aHMzTgTntqC-TjMIw4&location.latitude=Latitude&location.longitude=Longitude'
#city_name = input('Enter your city:' )
#response= requests.get(base_url)
data = response.json()
print(data)'''



