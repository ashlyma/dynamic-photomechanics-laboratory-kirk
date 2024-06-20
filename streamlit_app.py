import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import datetime

#Displays the first tittle of the page
st.header("Dynamic Photomechanics Laboratory")

#Text box that will acquire the users name (Potentially changed to drop-down with usernames)
username_textbox = st.text_input("Enter your name:", placeholder = "Enter your first and last name...")

#Package that takes the date that the experiment ran
Date_form = st.date_input("Date input:", value=None)

#Facility type select-box 
facility_type = st.selectbox("Select facility:",[''])
#The button used to create the directory
st.button("Create")
