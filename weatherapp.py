import streamlit as st
#from google.colab import userdata
#Get Lat and Lng based on city, country
#api_key = userdata.get('GOOGLE_API_KEY') # Get the API key from userdata
api_key = st.secrets["GOOGLE_API_KEY"]
#weather_api = userdata.get('G_WEATHER_API')
weather_api = st.secrets["G_WEATHER_API"]
city_name = input('Enter your city:' )
address = city_name
url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"

response = requests.get(url)
location = response.json()['results'][0]['geometry']['location']
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
print(data)



