import streamlit as st
import requests
import urllib3
import google.generativeai as genai
import os
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY")
WEATHERBIT_API_KEY = os.getenv("WEATHERBIT_API_KEY")
TREFLE_API_KEY = os.getenv("TREFLE_API_KEY")
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def find_planting_locations(city):
    url = f"https://api.foursquare.com/v3/places/search?query=parks&near={city}"
    headers = {
        "Accept": "application/json",
        "Authorization": FOURSQUARE_API_KEY,
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        json_data = response.json()
        results = json_data.get("results", [])
        return [{"name": result["name"], "address": result["location"]["formatted_address"]} 
                for result in results]
    except Exception as e:
        st.error(f"Error fetching planting locations: {str(e)}")
        return []

def get_lat_lon(city):
    geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}"
    try:
        response = requests.get(geocode_url, verify=False)
        data = response.json()
        if data["results"]:
            lat = data["results"][0]["geometry"]["lat"]
            lon = data["results"][0]["geometry"]["lng"]
            return lat, lon
    except Exception as e:
        st.error(f"Error in geocoding: {str(e)}")
    return None, None

def get_soil_type(lat, lon):
    url = f"https://rest.soilgrids.org/query?lon={lon}&lat={lat}"
    try:
        response = requests.get(url, timeout=10).json()
        if "properties" in response:
            soil_texture = response["properties"].get("soil_texture", "Unknown")
            soil_ph = response["properties"].get("ph", 7.0)
            return soil_texture, soil_ph
    except Exception:
        pass
    return "Unknown", 7.0

def recommend_plants(city):
    weather_url = f"https://api.weatherbit.io/v2.0/current?city={city}&key={WEATHERBIT_API_KEY}"
    try:
        weather_data = requests.get(weather_url).json()
        if "data" in weather_data and weather_data["data"]:
            climate = weather_data["data"][0]["weather"]["description"].lower()
            temperature = weather_data["data"][0]["temp"]
            
            if "rain" in climate and temperature > 20:
                return ["Neem Tree", "Tulsi Plant", "Curry Leaf Plant"]
            elif "clear" in climate and temperature > 25:
                return ["Aloe Vera", "Cactus", "Bamboo"]
            else:
                return ["Money Plant", "Snake Plant", "Areca Palm"]
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
    return []

def get_plant_details(plant_name):
    url = f"https://trefle.io/api/v1/plants/search?token={TREFLE_API_KEY}&q={plant_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and data["data"]:
            plant_info = data["data"][0]
            return {
                "scientific_name": plant_info.get("scientific_name", "N/A"),
                "family": plant_info.get("family", "N/A"),
                "common_name": plant_info.get("common_name", plant_name),
                "growth_conditions": plant_info.get("growth_habit", "Unknown"),
                "watering": plant_info.get("main_species", {}).get("specifications", {}).get("water_requirement", "Unknown"),
                "sunlight": plant_info.get("main_species", {}).get("growth", {}).get("light", "Unknown"),
            }
    except Exception as e:
        st.error(f"Error fetching plant details: {str(e)}")
    return None

def guide_page(city):
    st.title("🌱 Urban Green Guide")
    st.write("Find the best places to plant trees, get plant recommendations, and learn how to grow them.")
    
    if st.button("Find Planting Options"):
        # Get locations
        locations = find_planting_locations(city)
        if locations:
            st.write("### 🏞 Suitable Planting Locations:")
            for loc in locations:
                st.write(f"- {loc['name']}: {loc['address']}")
        else:
            st.warning("No planting locations found.")

        # Get plant recommendations
        plants = recommend_plants(city)
        if plants:
            st.write("### 🌿 Recommended Plants:")
            for plant in plants:
                st.write(f"- {plant}")
            
            # Show details for first plant
            selected_plant = plants[0]
            plant_info = get_plant_details(selected_plant)
            if plant_info:
                st.write(f"### 📖 Planting Guide for {selected_plant}:")
                st.write(f"- Scientific Name: {plant_info['scientific_name']}")
                st.write(f"- Family: {plant_info['family']}")
                st.write(f"- Growth Conditions: {plant_info['growth_conditions']}")
                st.write(f"- Watering: {plant_info['watering']}")
                st.write(f"- Sunlight: {plant_info['sunlight']}")
            else:
                st.write("No additional details available.")

def chatbot_page(city, locations):
    st.title("💬 Chatbot")
    user_question = st.text_input("Ask your question about plants, soil, or planting locations:")
    
    if st.button("Send Question"):
        if user_question:
            # Create Gemini model instance
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = (
                f"Answer the following question: {user_question}, and add some stuff about gardening and greenery in the response."
            )
            
            try:
                response = model.generate_content(prompt)
                st.write("💡 Chatbot:", response.text)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")

def main():
    # Sidebar
    city = st.sidebar.text_input("Enter your city:", "Mumbai")
    page = st.sidebar.selectbox("Select Page", ["Guide", "Chatbot"])

    if city:
        locations = find_planting_locations(city)
        
        if page == "Guide":
            guide_page(city)
        elif page == "Chatbot":
            chatbot_page(city, locations)

if __name__ == "__main__":
    main()
