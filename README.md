# AI-Powered Green Guide

## 🌱 Overview

AI-Powered Green Guide is a web application designed to help users find suitable locations for planting trees, determine the soil type in a specific area, and receive plant recommendations based on climate conditions. The app also includes an AI-powered chatbot to answer gardening-related queries.

## 🚀 Features

**Find Planting Locations:** Uses the Foursquare API to identify parks and open spaces suitable for planting.

**Soil Type Analysis:** Retrieves soil data based on latitude and longitude.

**Plant Recommendations:** Suggests plants based on climate conditions using Weatherbit API.

**Plant Details:** Provides scientific details, growth conditions, and care requirements for recommended plants.

**AI Chatbot:** Powered by Google Gemini AI, it answers gardening and greenery-related queries.

## 🛠️ Technologies Used

**Frontend:** Streamlit

**Backend:** Python, Requests

**APIs Used:**

[Foursquare API](https://location.foursquare.com/developer/) (to locate parks and planting areas)

[OpenCage Geocoder](https://opencagedata.com/) (to get latitude and longitude from city name)

[Weatherbit API](https://www.weatherbit.io/) (to fetch weather conditions)

[SoilGrids API](https://soilgrids.org/) (to retrieve soil type information)

[Trefle API](https://trefle.io/) (to fetch plant details)

[Google Gemini AI](https://ai.google.dev/) (for chatbot responses)

## 🔧 Installation

Clone the repository:
```sh
git clone https://github.com/sarkar-abhranshu/AI-Powered-Green-Guide.git
cd AI-Powered-Green-Guide
```
Install dependencies:
Considering you are already in the directory for the project,
```sh
pip install -r requirements.txt
```
Run the application:
```sh
streamlit run main.py
```

## 📌 Usage

Enter a city name in the sidebar.

Choose between the Guide or Chatbot page.

Guide: Displays planting locations, soil information, and plant recommendations.

Chatbot: Asks AI-powered queries about gardening and planting.

## 📜 API Keys Setup

Replace the placeholder API keys in app.py with your actual API keys:

## 🤝 Contributing

Feel free to fork this repository, make improvements, and create pull requests.

## 📧 Contact

For queries or suggestions, reach out to abhranshusarkar@outlook.com.
