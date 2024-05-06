import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly.express as px

# Load the data
data_path = './data/second.csv'
data = pd.read_csv(data_path)

# Convert 'Start Datetime' to datetime
data['Start Datetime'] = pd.to_datetime(data['Start Datetime']).dt.date


# Set the date as the index
data.set_index('Start Datetime', inplace=True)

# Group by date and device, then calculate the daily average speed
daily_avg_speed = data.groupby(['Start Datetime', 'Device'])['Avg Speed (mph)'].mean().unstack()
daily_max_speed = data.groupby(['Start Datetime', 'Device'])['Top speed (mph)'].max().unstack()
daily_miles = data.groupby(['Start Datetime', 'Device'])['Length (mi)'].sum().unstack()

# Filter the DataFrame to include only rows where Status is 'Moving'
moving_data = data[data['Status'] == 'Moving']

# Group by 'Start Datetime' and 'Device', sum 'Duration in Minutes', and unstack
daily_duration = moving_data.groupby(['Start Datetime', 'Device'])['Duration in Minutes'].sum().unstack()

# Reset index to convert the index into a column
daily_avg_speed.reset_index(inplace=True)
daily_max_speed.reset_index(inplace=True)
daily_miles.reset_index(inplace=True)
daily_duration.reset_index(inplace=True)


# Create a line chart using Plotly
fig = px.line(daily_avg_speed, x='Start Datetime', y=daily_avg_speed.columns[1:],
              title='AVERAGE SPEED(MPH) OF DEVICES',
              labels={'value':'Average Speed (mph)', 'variable':'Device'},
              markers=True,
              color_discrete_sequence=["red", "blue"])

# Update tooltips to show more info
fig.update_traces(mode='lines+markers+text', textposition='top center')


# Display the Plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)


dig = px.line(daily_max_speed, x='Start Datetime', y=daily_max_speed.columns[1:],
              title='TOP SPEED(MPH) OF DEVICES',
              labels={'value':'Top Speed (mph)', 'variable':'Device'},
              markers=True,
              color_discrete_sequence=["red", "blue"])

# Update tooltips to show more info
dig.update_traces(mode='lines+markers+text', textposition='top center')


# Display the Plotly chart in Streamlit
st.plotly_chart(dig, use_container_width=True)

# Create a line chart using Plotly
nig = px.line(daily_miles, x='Start Datetime', y=daily_miles.columns[1:],
              title='TOTAL MILES ON DEVICES',
              labels={'value':'Length (mi)', 'variable':'Device'},
              markers=True,
              color_discrete_sequence=["red", "blue"])

# Update tooltips to show more info
nig.update_traces(mode='lines+markers+text', textposition='top center')


# Display the Plotly chart in Streamlit
st.plotly_chart(nig, use_container_width=True)

# Create a line chart using Plotly
lig = px.line(daily_duration, x='Start Datetime', y=daily_duration.columns[1:],
              title='TOTAL MOVE DURATION IN MINUTES',
              labels={'value':'Time(mins)', 'variable':'Device'},
              markers=True,
              color_discrete_sequence=["red", "blue"])

# Update tooltips to show more info
lig.update_traces(mode='lines+markers+text', textposition='top center')


# Display the Plotly chart in Streamlit
st.plotly_chart(lig, use_container_width=True)

df = pd.DataFrame(
                np.random.rand(10, 4),
                columns= ["NO2","C2H5CH","VOC","CO"])
# generate a date range to be used as the x axis
df['date'] =  pd.date_range("2014-01-01", periods=10, freq="m")
df_melted = pd.melt(df,id_vars=['date'],var_name='parameter', value_name='value')
c = alt.Chart(df_melted, title='measure of different elements over time').mark_line().encode(
     x='date', y='value', color='parameter')

st.altair_chart(c, use_container_width=True)