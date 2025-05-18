import streamlit as st
import requests
import os
API_KEY = st.secrets["API_KEY"]

if not API_KEY:
    st.error("API key not found. Please set the API_KEY in your .env file.")
    st.stop()
# Weatherstack API Key

BASE_URL = "http://api.weatherstack.com/current"

def get_weather(city):
    params = {
        "access_key": API_KEY,
        "query": city
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "current" in data:
            return data
    return None

# Streamlit UI
st.set_page_config(page_title="🌦️ Weatherstack App", layout="centered")
st.title("🌍 Real-Time Weather Application")

with st.form("Enter the details below"):
    city=st.text_input("Enter City Name", placeholder="e.g. New York")
    submit = st.form_submit_button("Get details")

if submit:
    weather_data = get_weather(city)
    if weather_data:
        location = weather_data["location"]
        current = weather_data["current"]

        st.success(f"Weather in {location['name']}, {location['country']}")
        st.metric("🌡️ Temperature", f"{current['temperature']} °C")
        st.metric("💧 Humidity", f"{current['humidity']}%")
        st.metric("💨 Wind Speed", f"{current['wind_speed']} km/h")
        st.metric("☁️ Weather Description", current['weather_descriptions'][0])
        st.write(f"📅 Date & Time: {location['localtime']}")
    else:
        st.error("Could not fetch weather data. Please check the city name or try again later.")
