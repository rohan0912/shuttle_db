import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta


st.title("Fairfield Inn & Suites Raleigh - Durham Airport/Research Triangle Park")
st.write(f"""**2750 Slater Rd, Morrisville, NC 27560, USA**""")
st.image('./data/ff.jpg', caption='Sunrise by the mountains', width=1200)


# FUNCTION TO LOAD AND PROCESS DATA
@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    data['Start Datetime'] = pd.to_datetime(data['Start Datetime'])
    data['End Datetime'] = pd.to_datetime(data['End Datetime'])
    return data


data = load_data('./data/second.csv')


# DEVICE AND DATE FILTER
device_options = data['Device'].unique()
selected_device = st.sidebar.selectbox('Select a device:', device_options)

# Generate list of dates between the minimum and maximum dates found in the data
min_date = data['Start Datetime'].min().date()
max_date = data['End Datetime'].max().date()
date_range = pd.date_range(start=min_date, end=max_date).date

# Use selectbox for date selection
selected_date = st.sidebar.selectbox('Select a date', options=date_range)


# FILTERING DATA FOR CURRENT AND PREVIOUS DAY(Previous day data for percentage change)
filtered_data = data[(data['Start Datetime'].dt.date <= selected_date) &
                     (data['End Datetime'].dt.date >= selected_date) &
                     (data['Device'] == selected_device)]

filtered_data_previous_day = data[(data['Start Datetime'].dt.date == (selected_date - timedelta(days=2))) &
                                  (data['Device'] == selected_device)]

# FUNCTION FOR AVERAGE SPEED
def calculate_avg_speed(data):
    return data.groupby(data['Start Datetime'].dt.date)['Avg Speed (mph)'].mean().reset_index(name='Average Speed')


# Get average speed data
#avg_speed_data = calculate_avg_speed(filtered_data)
#avg_speed_previous_day_data = calculate_avg_speed(filtered_data_previous_day)


# CALCULATING AVERAGE SPEED (CURRENT AND PREVIOUS DAY)
avg_speed = filtered_data['Avg Speed (mph)'].mean()
avg_speed_previous_day = filtered_data_previous_day['Avg Speed (mph)'].mean()


# CALCULATING TOP SPEED (CURRENT AND PREVIOUS DAY)
top_speed = filtered_data['Top speed (mph)'].max()
top_speed_previous_day = filtered_data_previous_day['Top speed (mph)'].max()


# CALCULATING TOTAL DISTANCE (CURRENT AND PREVIOUS DAY)
total_dist = filtered_data['Length (mi)'].sum()
total_dist_previous_day = filtered_data_previous_day['Length (mi)'].sum()

# CALCULATING IDLE TIME (CURRENT AND PREVIOUS DAY)
idle_time = filtered_data['Engine Idle in Minutes'].sum()
idle_time_previous_day = filtered_data_previous_day['Engine Idle in Minutes'].sum()

# FUNCTION PERCENTAGE CHANGE
def percentage_change(previous_day, current_day):
    if previous_day and current_day:
        percent = ((current_day - previous_day) / previous_day) * 100
    else:
        percent = 0
    return percent


percentage_change_avg = percentage_change(avg_speed_previous_day, avg_speed)
percentage_change_top = percentage_change(top_speed_previous_day, top_speed)
percentage_change_dist = percentage_change(total_dist_previous_day, total_dist)
percentage_change_idle = percentage_change(idle_time_previous_day, idle_time)



# Display the percentage change
#st.metric("Average Speed Today", f"{avg_speed_today:.2f} mph", f"{percentage_change:.2f} % change from previous day")

# Function to calculate time by status
def calculate_time_by_status(data, status):
    results = []
    for _, row in data[data['Status'] == status].iterrows():
        start = row['Start Datetime']
        end = row['End Datetime']
        start_hour = start.hour
        end_hour = end.hour
        for hour in range(start_hour, end_hour + 1):
            if hour == start_hour and hour == end_hour:
                duration = (end - start).total_seconds() / 60
            elif hour == start_hour:
                duration = (start.replace(minute=0, second=0, microsecond=0) + pd.Timedelta(hours=1) - start).total_seconds() / 60
            elif hour == end_hour:
                duration = (end - end.replace(minute=0, second=0, microsecond=0)).total_seconds() / 60
            else:
                duration = 60
            results.append({"Hour": hour, "Time": duration, "Status": status})
    hourly_data = pd.DataFrame(results)
    return hourly_data.groupby(["Hour", "Status"]).sum().clip(upper=60).reset_index()

# Calculate time data for both statuses
combined_data = pd.concat([calculate_time_by_status(filtered_data, 'Stopped'), calculate_time_by_status(filtered_data, 'Moving')])

# Filter out rows with NaN values in latitude and longitude columns
df_filtered = filtered_data[filtered_data['latitude'].notna() & filtered_data['longitude'].notna()]

# Display the map
st.map(df_filtered, size = 40)

st.markdown('#')

#DISPLAY AVG SPEED, TOP SPEED, TOTAL MILES, ENGINE IDLE(MINS)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Speed", f"{avg_speed:.2f} mph", f"{percentage_change_avg:.2f}%")
col2.metric("⚡ Top Speed", f"{top_speed:.2f} mph", f"{percentage_change_top:.2f}%")
col3.metric("🚌 Total Miles", f"{total_dist:.2f} miles", f"{percentage_change_dist:.2f}%")
col4.metric("⏰ Engine Idle Time", f"{idle_time:.2f} minutes", f"{percentage_change_idle:.2f}%")
st.markdown('#')

# Create Altair chart for visualization
st.write(f"""**Drive Time and Idle Time by Hour**""")
st.markdown('###')
st.altair_chart(
    alt.Chart(combined_data)
    .mark_bar()
    .encode(
        x=alt.X('Hour:O', axis=alt.Axis(title='Hour of the Day', tickCount=24)),
        y=alt.Y('Time:Q', axis=alt.Axis(title='Time (minutes)')),
        color=alt.Color('Status:N', scale=alt.Scale(domain=['Stopped', 'Moving'], range=['yellow', 'green'])),
        tooltip=[alt.Tooltip('Hour', title='Hour'), alt.Tooltip('Time', title='Time (minutes)'), alt.Tooltip('Status', title='Status')]
    ).properties(
        width=700,
        height=500
    ).configure_mark(opacity=0.75, color="red"),
    use_container_width=True
)