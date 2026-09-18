from PST1.msms_project import MSMS_copy
from PST2 import ps2_main
import json

# DATA_FILE1 = { 
#     "students" : [
#         {"id": 1, "name" : 'Alice'},
#         {"id" :2}
#     ],
#     "teachers": null,
#     "courses": [
#         {"id": 'abc', 'title' : 'Piano 101'}
#     ]
# }

with open('msms_broken', 'w') as f:
    json.dump('msms_broken', f, indent=4)
    print("Data saved successfully.")
    

import streamlit as st

st.title("MY FIRST WEB PAGE!!!")
name = st.text_input("Enter your name")

if st.button("Greet"):
    st.write(f'Hello, {name}! Welcome to streamlit!')

st.header('This is a header')
st.subheader('aaaaa')
st.text('aldhdjhaewajese')
st.checkbox('click if straight')
st.radio('Choose 1', ["option A", 'Option B'])
st.selectbox('pick a number:', [ 1, 2, 3])
st.slider('Select a value', 0, 100)

import numpy as np 
import pandas as pd 
chart_data = pd.DataFrame(np.random.randn(20,3), columns=['a','b','c'])
st.line_chart(chart_data)

from PIL import Image 
img = Image.open('my_image.png')
st.image(img, caption='My Image', use_container_width = True)



