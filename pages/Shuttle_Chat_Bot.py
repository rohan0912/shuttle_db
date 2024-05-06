import streamlit as st
import pandas as pd
from dateutil import parser
import re
import time
import streamlit as st
#import pyttsx3
import threading


# Inject custom CSS with increased font size

st.set_page_config(layout="wide")


st.title("Shuttle Chat Bot")

@st.cache_data
def load_data(filepath):
    df = pd.read_csv(filepath)
    df['Start Datetime'] = pd.to_datetime(df['Start Datetime'])
    return df


def query_data(df, query):
    date_search = re.search(r'\d{1,2}/\d{1,2}/\d{4}', query)
    device_search = re.findall(r'#\d', query)

    if date_search:
        query_date = parser.parse(date_search.group())
        filtered_df = df[df['Start Datetime'] == query_date]

        if not filtered_df.empty:
            if device_search:
                filtered_df = filtered_df[filtered_df['Device'].isin(device_search)]
            if 'average speed' in query.lower():
                result = filtered_df.groupby('Device')['Average Speed'].mean().to_dict()
                stat_type = 'average speed'
            elif 'top speed' in query.lower():
                result = filtered_df.groupby('Device')['Top Speed'].max().to_dict()
                stat_type = 'top speed'
            elif 'total distance' in query.lower():
                result = filtered_df.groupby('Device')['Total Distance'].sum().to_dict()
                stat_type = 'total distance'
            else:
                return "Specify 'top speed', 'average speed', 'total distance' for the query."
            result_sentence = f"The {stat_type} on {query_date.strftime('%m/%d/%Y')} for "
            results_list = [f"device {device}: {value}" for device, value in result.items()]
            result_sentence += " and ".join(results_list) + "."
            return result_sentence
        else:
            return "No data available for this date."
    else:
        return "Specify a valid date in MM/DD/YYYY format."


def generate_stats_summary(df, date_query):
    date_search = re.search(r'\d{1,2}/\d{1,2}/\d{4}', date_query)
    if date_search:
        query_date = parser.parse(date_search.group())
        filtered_df = df[df['Start Datetime'] == query_date]

        if not filtered_df.empty:
            summary = ""
            for device in filtered_df['Device'].unique():
                device_data = filtered_df[filtered_df['Device'] == device]
                total_distance = device_data['Total Distance'].sum()
                top_speed = device_data['Top Speed'].max()
                avg_speed = device_data['Average Speed'].mean()

                previous_top_speed = device_data['Previous Top Speed'].iloc[0]
                previous_avg_speed = device_data['Previous Average Speed'].iloc[0]
                previous_total_distance = device_data['Previous Total Distance'].iloc[0]

                top_speed_change = ((top_speed - previous_top_speed) / previous_top_speed * 100) if previous_top_speed else "N/A"
                avg_speed_change = ((avg_speed - previous_avg_speed) / previous_avg_speed * 100) if previous_avg_speed else "N/A"
                total_distance_change = ((total_distance - previous_total_distance) / previous_total_distance * 100) if previous_total_distance else "N/A"

                avg_speed_part = f"maintaining an average speed of {avg_speed:.1f} mph"
                if avg_speed < 20:
                    avg_speed_part += " (It is below the required average speed)"
                top_speed_part = f"reaching a top speed of {top_speed} mph"
                if top_speed > 65:
                    top_speed_part += " (SLOW DOWN!)"
                if top_speed_change < 0:
                    top_speed_change_desc = f", a percent decrease of {top_speed_change:.1f}% from the previous day" if isinstance(top_speed_change, float) else ", with no previous data to compare."
                else:
                    top_speed_change_desc = f", a percent increase of {top_speed_change:.1f}% from the previous day" if isinstance(top_speed_change, float) else ", with no previous data to compare."
                avg_speed_change_desc = f", a change of {avg_speed_change:.1f}% from the previous day" if isinstance(avg_speed_change, float) else ", with no previous data to compare."
                total_distance_change_desc = f", a change of {total_distance_change:.1f}% from the previous day" if isinstance(total_distance_change, float) else ", with no previous data to compare."

                device_summary = f"  \nDevice {device} has a total recorded travel distance of {total_distance} miles{total_distance_change_desc}, {top_speed_part}{top_speed_change_desc} and {avg_speed_part}{avg_speed_change_desc}."
                summary += device_summary

            return summary
        else:
            return "No data available for this date."
    else:
        return "Specify a valid date in MM/DD/YYYY format."

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter your query:"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    filepath = './data/tr1.csv'  # Update this path
    df = load_data(filepath)

    response = query_data(df, prompt) if any(
        x in prompt.lower() for x in ['average speed', 'top speed', 'total distance', 'percentage top speed']) else generate_stats_summary(df,prompt)

    # Create an empty slot to update with the response
    message_placeholder = st.empty()

    # Simulate typing by updating the message one word at a time
    current_text = ""
    for word in response.split():
        current_text += word + " "
        message_placeholder.markdown(current_text)
        time.sleep(0.05)  # Wait a bit before adding the next word
    # Wait a bit before adding the next word

    st.session_state.messages.append({"role": "assistant", "content": response})
    #threaded_speech(response)



