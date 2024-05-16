# Airport Shuttle Pickup Dashboard

https://shuttledata.streamlit.app/

## Overview
This Streamlit dashboard provides a detailed visual analysis of airport shuttle pickups, showcasing various metrics that help in understanding the performance and operational efficiency of the shuttles. The app is divided into four main pages, each dedicated to presenting specific data insights through interactive charts and a chatbot for querying data.

### Dataset
The dashboard utilizes data from two different shuttles, encompassing metrics such as:
- Status (moving or stopped)
- Latitude and longitude coordinates
- Duration of trips
- Idle time duration
- Average speed
- Top speed

## Pages
### 1. Pickup Frequency Chart
This page displays the number of airport pickups every hour in a bar chart format. The data was preprocessed using pandas to calculate the number of pickups per hour, providing a clear view of pickup trends throughout the day.

### 2. Monthly Performance Comparison
The second page features a comparison chart detailing statistics like average speed, top speed, total miles, and total duration across different days of the month. This allows for a comparative analysis of shuttle performance and operational efficiency.

### 3. Drive Time and Idle Time Analysis
On the third page, users can view charts representing drive time and idle time for each shuttle, broken down by hour. This analysis is crucial for optimizing shuttle scheduling and improving overall efficiency.

### 4. Interactive Chatbot
The final page hosts a chatbot that can provide information on any requested metric, such as average speed or top speed on specific dates. This feature makes the dashboard interactive and user-friendly, catering to specific data queries.

## Technologies Used
- **Python:** Main programming language used.
- **Pandas:** Employed for data preprocessing and analysis.
- **Streamlit:** Used to create the dashboard interface.


