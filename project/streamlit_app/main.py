import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import datetime
import requests

# Creates two tabs called Form and Search
tab1, tab2 = st.tabs(["Form", "Search"])

#Shows the contant of tab2 (Search)
with tab2:
    #\\

# Content of tab1 (Form)
with tab1:
    # Function that displays a text box if "Other" is selected for multiple questions
    def other_textbox(selected_option, label, key):
        if selected_option == "Other":
            selected_option = st.text_input("Other:", placeholder= "Please enter other...")
        return None
    #Displays the first tittle of the page
    st.header("Dynamic Photomechanics Laboratory")

    #Text box that will acquire the users name (Potentially changed to drop-down with usernames)
    username_textbox = st.text_input("Name:", placeholder = "Enter your first and last name...")

    #Package that takes the date that the experiment ran
    Date_form = st.date_input("Experiment run-date:", value=None)

    # Defines the main categories of facilities and their corresponding sub-options
    facility_options = { 
        "None": [],
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
    facility_type_main_option = st.selectbox("Facility Type:", list(facility_options.keys()))

    # Second drop-down for selecting the sub-option based on the main facility and calls other function to show the text box for "other"
    if facility_type_main_option:
        facility_type_sub_option = st.selectbox(f"Experiment type for {facility_type_main_option}:", facility_options[facility_type_main_option])
        facility_other = other_textbox(facility_type_sub_option, "facility type", key="facility_other")

    # Material type dropdown and calls other function to show the text box for "other"
    material_type_option = st.selectbox("Material type:",("None","Metallic","Composite","Polymer","Ceramic","Other"))
    material_other = other_textbox(material_type_option, "material type", key="material_other")

    # Text box input for the load type
    input_load_type = st.text_input("Input (Load) Magnitude in SI Units:", placeholder = "Enter Magnitude")

    # load type dropdown and calls other function to show the text box for "other"
    load_type_dropdown = st.selectbox("Load Type:", ("None","Force (kN)", "Pressure (MPa)", 
        "Energy (J)", "Displacement (mm)", "Velocity (m/s)", "Acceleration (m/s^2)", "Other"))
    load_other = other_textbox(load_type_dropdown, "load type", key="load_other")

    # Trial number text box
    trial_input = st.number_input("Trial #:", min_value=1, step=1, placeholder="Enter trial number...")

    #The button used to create the directory
    st.write("Directory file name:")
    st.write(username_textbox, "/", facility_type_main_option, "/",facility_type_sub_option, "/", "[", Date_form,"/", material_type_option,"/", "Trial:", trial_input, "]")
    st.button("Create")
