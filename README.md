# An interactive real-time weather display using Streamlit

<div align = "justify">

# Overview

This project presents an interactive weather dashboard for various cities in India using the WeatherAPI. The app provides users with an overview of weather conditions such as temperature, humidity, wind speed, and more. The dashboard allows filtering cities by weather conditions, temperature range, and regions. It also includes visualizations like histograms, box plots, bar charts, and a choropleth map to showcase weather data geographically.

# Methodology

The weather data for multiple Indian cities is fetched via the WeatherAPI. This data is processed and filtered using Pandas and visualized with Plotly for interactive charts. Folium is used for mapping the geographic data of the cities, displaying weather conditions across India. The interactive dashboard is built using Streamlit, allowing real-time exploration and analysis of weather trends.

# Setup

**1)** **Visual Studio Code**: for development

**2)** **Streamlit, Plotly, Folium**: for visualization

**3)** **Weather API key**: for weather scraping

# Implementation

**1) Setup Environment and Dependencies:**

Install required Python libraries: Streamlit, Pandas, Numpy, Requests, Plotly, Folium, and Geopy.
Configure the WeatherAPI by obtaining an API key and inserting it into the code.

**2) Weather Data Fetching:**

Create a function fetch_weather(city) to make API calls to WeatherAPI for retrieving real-time weather data for the specified city.
Extract necessary weather details like temperature, humidity, wind speed, and weather condition from the API response.

**3) Fetching Data for Multiple Cities:**

Define a list of cities across India.
Use a loop to fetch weather data for each city in the list, handling API failures with error messages using Streamlit’s st.error().

**4) Building the Dashboard with Streamlit:**

Create a sidebar to allow users to filter cities by weather conditions, temperature range, and specific regions/states.
Implement sliders and multiselect widgets to allow users to adjust the displayed data interactively.

**5) Data Filtering:**

Based on the user’s input, filter the weather data using Pandas to match the selected temperature range, conditions, and regions.
Display the filtered data in an interactive table using st.dataframe().

**6) Visualization with Plotly:**

Generate dynamic visualizations for weather data using Plotly:
Histogram: Display the distribution of a selected weather factor (e.g., temperature, humidity).
Boxplot: Show a boxplot for the selected weather factor.
Bar Charts: Create charts for the top 5 hottest and coldest cities.

**7) Geographical Mapping with Folium:**

Retrieve the geographical coordinates of cities using Geopy.
Use Folium to create an interactive map centered on India.
Plot markers with weather icons (e.g., sun for clear weather, cloud for cloudy) on the map, representing the cities and their weather conditions.

**8) Adding Interactive Choropleth Map:**

Use the temperature data and city coordinates to create a choropleth map showing temperature distribution across cities.
Visualize temperature variations using color gradients and add markers for individual cities with tooltips displaying detailed weather info.

**9) Optimize Performance:**

Cache weather and geographic data using @st.cache_data decorator to reduce API calls and improve app performance.

# Result

<p align = "center">
    <img src= "https://github.com/user-attachments/assets/c9831e6d-0e81-412f-8c7f-c98b133ac016" alt = "Sample showcase" />
</p>

**Explore the complete application here:** https://weatherwidget.streamlit.app/

# Conclusion

This weather dashboard offers a simple and interactive way to explore current weather conditions across Indian cities. By integrating live data, it provides real-time insights and supports decision-making for weather-related queries.

</div>

# Credits

**1)** WeatherAPI.com

**2)** Streamlit.io
