# Importing Necessary Libraries
import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import plotly.express as px  
import folium  
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium  
from geopy.geocoders import ArcGIS


# ******************************************************************    
api_key = 'a829df4ff84c4d73a28171130242207'
# ******************************************************************

# Function to fetch weather data from WeatherAPI
@st.cache_data
def fetch_weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'
    response = requests.get(url)
    data = response.json()

    return {
        'City': data['location']['name'],
        'Region': data['location']['region'],
        'Country': data['location']['country'],
        'Temperature (C)': data['current']['temp_c'],
        'Condition': data['current']['condition']['text'],
        'Wind (kph)': data['current']['wind_kph'],
        'Humidity (%)': data['current']['humidity'],
        'Pressure (mb)': data['current']['pressure_mb'],
        'Last Updated': data['current']['last_updated']
    }

# Fetch weather data for multiple cities
def get_weather_data(cities):
    weather_data = []
    for city in cities:
        try:
            weather = fetch_weather(city)
            weather_data.append(weather)
        except:
            st.error(f"Failed to fetch data for {city}")
    return pd.DataFrame(weather_data)

cities = [
    "New Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru", "Hyderabad", "Ahmedabad",
    "Pune", "Jaipur", "Surat", "Lucknow", "Kanpur", "Nagpur", "Patna", "Indore", "Bhopal",
    "Ludhiana", "Agra", "Cuttack", "Jamnagar", "Vadodara", "Coimbatore", "Thane", "Kochi",
    "Visakhapatnam", "Guwahati", "Madurai", "Mysuru (Mysore)", "Gurugram (Gurgaon)",
    "Noida", "Varanasi", "Amritsar", "Jodhpur", "Raipur", "Ranchi", "Chandigarh",
    "Bhubaneswar", "Dehradun", "Mangaluru (Mangalore)", "Thiruvananthapuram", "Gwalior"
]

# Fetch data
df = get_weather_data(cities)

# Sidebar filters
st.sidebar.header("Filters")
selected_states = st.sidebar.multiselect("Select States", options=df['Region'].unique(), default=df['Region'].unique())
selected_conditions = st.sidebar.multiselect("Select Weather Conditions", options=df['Condition'].unique(), default=df['Condition'].unique())
temperature_range = st.sidebar.slider("Select Temperature Range (C)", 
                                      min_value=int(df['Temperature (C)'].min()), 
                                      max_value=int(df['Temperature (C)'].max()), 
                                      value=(int(df['Temperature (C)'].min()), int(df['Temperature (C)'].max())))

# Apply filters
df_filtered = df[(df['Region'].isin(selected_states)) & 
                 (df['Condition'].isin(selected_conditions)) & 
                 (df['Temperature (C)'].between(temperature_range[0], temperature_range[1]))]

st.title("🌤️ Weather Widget")
widget_disc = "This dashboard provides an interactive representation of weather conditions across different cities in India."

def stream_data(text):
    for word in text:
        yield word
        time.sleep(0.03)

if 'streaming_done' not in st.session_state:
    st.session_state.streaming_done = False

# Stream the data only if it hasn't been done before
if not st.session_state.streaming_done:
    st.write_stream(stream_data(widget_disc))
    st.session_state.streaming_done = True

# Display DataFrame
st.dataframe(df_filtered)

# New Filter: Weather Factor for Histograms and Boxplots
st.sidebar.header("Plot Settings")
weather_factor = st.sidebar.selectbox(
    "Select Weather Factor to Display",
    options=['Temperature (C)', 'Humidity (%)', 'Wind (kph)', 'Pressure (mb)'],
    index=0
)

# Histograms for Selected Weather Factor
fig_hist = px.histogram(df_filtered, x=weather_factor, nbins=20, title=f'Distribution of {weather_factor}')
fig_hist.update_layout(
    xaxis_title=weather_factor, 
    yaxis_title='Frequency',
    xaxis=dict(showgrid=False), 
    yaxis=dict(showgrid=False)
)
st.plotly_chart(fig_hist)

# Boxplot for Selected Weather Factor 
fig_box = px.box(df_filtered, y=weather_factor, title=f'{weather_factor} Distribution')
fig_box.update_layout(
    yaxis_title=weather_factor,
    xaxis=dict(showgrid=False), 
    yaxis=dict(showgrid=False)
)
st.plotly_chart(fig_box)

# Top 5 Hottest and Coldest Cities 
top_hot_cities = df_filtered.sort_values(by='Temperature (C)', ascending=False).head(5)
top_cold_cities = df_filtered.sort_values(by='Temperature (C)', ascending=True).head(5)


# Top 5 hottest cities
fig_hot = px.bar(
    top_hot_cities, 
    x='Temperature (C)', 
    y='City', 
    orientation='h', 
    color='Temperature (C)', 
    color_continuous_scale='Reds', 
    title='Top 5 Hottest Cities',
    labels={'Temperature (C)': 'Temperature (°C)', 'City': 'City'}
)
fig_hot.update_layout(yaxis=dict(showticklabels=False))  # Hide y-axis labels
st.plotly_chart(fig_hot)

# Top 5 coldest cities
fig_cold = px.bar(
    top_cold_cities, 
    x='Temperature (C)', 
    y='City', 
    orientation='h', 
    color='Temperature (C)', 
    color_continuous_scale='Blues', 
    title='Top 5 Coldest Cities',
    labels={'Temperature (C)': 'Temperature (°C)', 'City': 'City'}
)
fig_cold.update_layout(yaxis=dict(showticklabels=False))  # Hide y-axis labels
st.plotly_chart(fig_cold)

# Pie Chart for Weather Conditions 
condition_counts = df_filtered['Condition'].value_counts().reset_index()
condition_counts.columns = ['Condition', 'Count']
fig_pie = px.pie(condition_counts, values='Count', names='Condition', title='Weather Conditions Distribution')
st.plotly_chart(fig_pie)

# Fetch Geographic Data
@st.cache_data
def fetch_geographic_data(cities):
    nom = ArcGIS()
    results = []
    for city in cities:
        location = nom.geocode(city)
        results.append({
            'City': city,
            'Latitude': location.latitude if location else None,
            'Longitude': location.longitude if location else None
        })
    return pd.DataFrame(results)

df_geo = fetch_geographic_data(cities)

# Merge weather and geographic data
final_df = pd.merge(df_filtered, df_geo, on='City', how='inner')

# Filter out rows with missing latitude or longitude
final_df = final_df.dropna(subset=['Latitude', 'Longitude'])

if final_df.empty:
    st.warning("No valid geographic data found for the selected cities.")
else:
    # Choropleth Map for Temperature Distribution using Folium
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for _, row in final_df.iterrows():
        feature = {
            "type": "Feature",
            "properties": {
                "City": row["City"],
                "Temperature (C)": row["Temperature (C)"]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row["Longitude"], row["Latitude"]]
            }
        }
        geojson["features"].append(feature)

    # Create Folium map centered around India
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    # Adding marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    def get_weather_icon_and_color(condition):
        # Mapping of weather conditions to icons and colors
        if 'sun' in condition.lower() or 'clear' in condition.lower():
            return 'sun', 'darkorange'
        elif 'cloud' in condition.lower():
            return 'cloud', 'darkblue'
        elif 'rain' in condition.lower() or 'drizzle' in condition.lower():
            return 'cloud-rain', 'darkpurple'
        elif 'storm' in condition.lower() or 'thunder' in condition.lower():
            return 'bolt', 'darkred'
        elif 'snow' in condition.lower():
            return 'snowflake', 'cadetblue'
        elif 'fog' in condition.lower() or 'mist' in condition.lower():
            return 'smog', 'darkgreen'
        else:
            return 'cloud', 'darkgray'  

    # Adding markers with weather-related icons
    for idx, row in final_df.iterrows():
        icon, color = get_weather_icon_and_color(row['Condition'])
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['City']}: {row['Temperature (C)']}°C, {row['Condition']}",
            tooltip=folium.Tooltip(f"City: {row['City']}<br>Temperature: {row['Temperature (C)']}°C<br>Condition: {row['Condition']}"),
            icon=folium.Icon(color=color, icon=icon, prefix='fa')  
        ).add_to(marker_cluster)

    folium.Choropleth(
        geo_data=geojson,
        data=final_df,
        columns=['City', 'Temperature (C)'],
        key_on='feature.properties.City',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Temperature (C)'
    ).add_to(m)

    st_folium(m, width=800, height=500)

st.write("Adjust the filters on the sidebar to explore more!")
