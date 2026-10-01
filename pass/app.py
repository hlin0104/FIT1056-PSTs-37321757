import streamlit as st
import json
import pandas as pd
try:
    with open("network_logs.json", 'r') as file:
        data = json.load(file)
        stats = pd.DataFrame(data) #converts raw dictionary data into a clean 
        data_type = st.selectbox('Select a place', ['Library Wi-Fi Connections', 'Cafeteria Transactions', 'Mainframe Pings'])
        days_chosen = st.slider('Choose the day range', min_value = 1, max_value = 30, value = (1,30))
        min_value, max_value = days_chosen

        active_days = stats[(stats['Day'] >= min_value) & (stats['Day'] <=  max_value)]
        
        graph = active_days.set_index('Day')[[data_type]]
        st.line_chart(graph)
except FileNotFoundError:
    st.error('Error: stupid stupid')

