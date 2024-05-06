import os
import altair as alt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import random

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="Airport Shuttle Dashboard", page_icon=":taxi:")

@st.cache_data
def load_data():
    path = "./data/test1.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/streamlit/demo-uber-nyc-pickups/raw/main/{path}"
    data = pd.read_csv(
        path,
        nrows=100000,
        usecols=["date/time", "lat", "lon", "Device"],
        parse_dates=["date/time"],
        date_parser=lambda x: pd.to_datetime(x, format='%m/%d/%Y %H:%M')
    )
    return data

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={"latitude": lat, "longitude": lon, "zoom": zoom, "pitch": 50},
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ],
    ))

@st.cache_data
def filterdata_by_date(df, selected_date):
    return df[df['date/time'].dt.date == selected_date]

def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

def histdata_by_hour(df):
    #df['hour'] = df['date/time'].dt.hour
    #df['hour'] = df.apply(
    #   lambda row: [row['hour'], row['hour']] if row['Duration in Minutes'] > 15 else row['hour'], axis=1)
    hist = np.histogram(df['date/time'].dt.hour, bins=24, range=(0, 24))[0]
    return pd.DataFrame({"hour": range(24), "pickups": hist})

data = load_data()

st.title("Airport Shuttle Dashboard")
# Date filter
selected_date = st.sidebar.date_input("Select date of pickup", value=data["date/time"].dt.date.min(), min_value=data["date/time"].dt.date.min(), max_value=data["date/time"].dt.date.max())
filtered_data_by_date = data[data['date/time'].dt.date == selected_date]

# Device filter
device_selected = st.sidebar.multiselect("Select device", options=['#1', '#2'], default=['#1', '#2'])
filtered_data = filtered_data_by_date[filtered_data_by_date['Device'].isin(device_selected)]
midpoint = mpoint(filtered_data["lat"], filtered_data["lon"])
st.markdown('###')


#row2_1, row2_2, = st.columns((3, 2))

#with row2_1:
st.write(f"""**Raleigh-Durham International Airport on {selected_date.strftime('%Y-%m-%d')}**""")
st.map(filtered_data, size=40)

#with row2_2:
    #st.write(f"""**Raleigh-Durham International Airport on {selected_date.strftime('%Y-%m-%d')}**""")
    #st.image('C:/Users/rohan/Downloads/rrf1.jpeg')

st.markdown('###')
v_count = len(filtered_data)

first_value = str(filtered_data['date/time'].iloc[0])
first_value = first_value[11:]# Using iloc to get the first value
last_value = str(filtered_data['date/time'].iloc[-1])
last_value = last_value[11:]

col1, col2, col3, col4 = st.columns((2,2,2,2))

col2.metric("Total Trips", f"{v_count}", "w%")
col3.metric("🟢 Start Time", f"{first_value}", "20%")
col4.metric("🔴 End Time", f"{last_value}", "20%")
with col1:
    st.image('./data/rrf1.jpeg')

st.markdown('###')
chart_data = histdata_by_hour(filtered_data)
# LAYING OUT THE HISTOGRAM SECTION
st.write(f"""**Breakdown of rides per hour on {selected_date.strftime('%Y-%m-%d')}**""")
st.altair_chart(
        alt.Chart(chart_data)
        .mark_bar(size=50)  # Increased bar width
        .encode(
            x=alt.X("hour:Q", title="Hour of the day", scale=alt.Scale(domain=(0, 23))),
            y=alt.Y("pickups:Q", title="Number of pickups", axis=alt.Axis(format='d')),
            tooltip=[alt.Tooltip("hour", title="Hour of the day"), alt.Tooltip("pickups:Q", title="Number of pickups", format=',d')]
        ).properties(
        width=300,
        height=300
        ).configure_mark(opacity=0.7, color="green"),
        use_container_width=True
)
