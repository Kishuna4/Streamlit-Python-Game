import streamlit as st
import pandas as pd
import numpy as np
impot pydeck as pdk

DATA_URL = (
"/home/rhyme/Desktop/Project/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Streamlit dashboard that can be used to analyze motor vehicle collisions in NYC")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', "CRASH_TIME"]])
    data.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace = True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace = True)
    return data

data = load_data(100000)

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many collisions occur during a given time of day?")
hour = st.selectbox("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle colisiosn between %i:00 and %i:00")
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",
    initial_view_state{
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers = [
        pdk.Layer(
            "HexagonLayer",
            data = data[['date/time', 'latitude', longitude]],
            get_position = ['longitude', 'latitude'],
            radius = 100,
            extruded=True,
            pickable = True,
            elevation_scale=4,
            elevation_range = [0, 1000],
        ),
    ],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))

filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
fig = px.bar(chart_data, x = 'minute', y = 'crashes', hover_date=['minute', 'crashes'], height = st.write(fig))



if st.checkbox("Show Raw Data", False):

    st.subheader('Raw Data')
    st.write(data)
