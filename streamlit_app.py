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

# Defines the main categories of facilities and their corresponding sub-options
facility_options = {
    "Implosion Tank (aka 'Big' Tank)": ["Implosion", "UNDEX", "Other"],
    "Explosion Tank (aka 'Square' Tank)": ["UNDEX", "Other"],
    "Shock Tube (Gas)": ["AIREX", "Other"],
    "Hypersonic Shock Tube (Gas)": ["AIREX", "Other"],
    "Shock Tube (Water)": ["Air-backed Plate Shock", "Submerged UNDEX", "Other"], 
    "Flyer Plate Impactor (Gas Gun)": ["Spalling", "Ballistic", "Other"], 
    "SHPB (Dynamic)": ["Compression", "Tension", "Shear","Fracture", "Other"],
    "Drop Weight tower (Dynamic)": ["Plate Impact", "Three Point Bending", "Compression", "Other"],
    "HITS (Dynamic)": ["Puncture","Compression", "Other"], 
    "Dynamic Mechanical Analyzer (DMA)":["Three Point Bending", "Cantilever","Double Cantilever","Compression", "Tension", "Other"],
    "UTM (Static)": ["Tension", "Compression", "Shear", "Three Point Bending","Four Point Bending" "Peel", "Other"],
}

# First drop-down for selecting the main facility type
facility_type_main_option = st.selectbox("Select Facility Type", list(facility_options.keys()))

# Second drop-down for selecting the sub-option based on the main facility selection
if facility_type_main_option:
    facility_type_sub_option = st.selectbox(f"Select the facility sub-option for {facility_type_main_option}", facility_options[facility_type_main_option])

# Updates the facility_type_sub_option drop-down to a text box if the "Other" option is selected 
if facility_type_sub_option == "Other":
    facility_type_sub_option = st.text_input("Enter facility type:", placeholder = "Please enter the facility used...")

#The button used to create the directory
st.button("Create")
