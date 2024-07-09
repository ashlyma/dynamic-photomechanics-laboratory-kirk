import streamlit as st
import os
import datetime

# Nas local path as variable
nas_path = "Z:\DPML_Projects"

# Streamlit User Interface
tab1, tab2 = st.tabs(["Home", "Search"])

# Content under the tab 1 (Home)
with tab1:

    def other_textbox(selected_option, label, key):
        if selected_option == "Other":
            selected_option = st.text_input("Other:", placeholder="Please enter other...")
        return selected_option
    
    # Tittle of the top of the page
    st.header("Dynamic Photomechanics Laboratory")

    # Username and date questions
    username_textbox = st.text_input("Name:", placeholder="Enter your first and last name...")
    Date_form = st.date_input("Experiment run-date:", value=datetime.datetime.now())
    
    # Facility options array
    facility_options = { 
        "None": [],
        "Implosion Tank (aka 'Big' Tank)": ["","Implosion", "UNDEX", "Other"],
        "Explosion Tank (aka 'Square' Tank)": ["","UNDEX", "Other"],
        "Shock Tube (Gas)": ["","AIREX", "Other"],
        "Hypersonic Shock Tube (Gas)": ["","AIREX", "Other"],
        "Shock Tube (Water)": ["","Air-backed Plate Shock", "Submerged UNDEX", "Other"], 
        "Flyer Plate Impactor (Gas Gun)": ["","Spalling", "Ballistic", "Other"], 
        "SHPB (Dynamic)": ["","Compression", "Tension", "Shear","Fracture", "Other"],
        "Drop Weight tower (Dynamic)": ["","Plate Impact", "Three Point Bending", "Compression", "Other"],
        "HITS (Dynamic)": ["","Puncture","Compression", "Other"], 
        "Dynamic Mechanical Analyzer (DMA)":["","Three Point Bending", "Cantilever","Double Cantilever","Compression", "Tension", "Other"],
        "UTM (Static)": ["","Tension", "Compression", "Shear", "Three Point Bending","Four Point Bending" "Peel", "Other"],
    }

    # facility sub options appear based on the facility selected
    facility_type_main_option = st.selectbox("Facility Type:", list(facility_options.keys()))
    if facility_type_main_option:
        facility_type_sub_option = st.selectbox(f"Experiment type for {facility_type_main_option}:", facility_options[facility_type_main_option])
        facility_type_sub_option  = other_textbox(facility_type_sub_option, "facility type", key="facility_other")
    
    if facility_type_sub_option == "UNDEX":
    # Material, trial, input load and load type questions
        material_type_option = st.selectbox("Material type:", ("None","Metallic","Composite","Polymer","Ceramic","Other"))
        material_type_option = other_textbox(material_type_option, "material type", key="material_other")
        charge_type = st.selectbox("Charge type:", ("None","RP87","RP80","RP501","RP502","RP503","Other"))
        charge_type = other_textbox(charge_type, "Charge type:", key="charge_type_other")
        trial_input = st.number_input("Trial #:", min_value=0, step=1, placeholder="Enter trial number...")

    else:
        # Material, trial, input load and load type questions
        material_type_option = st.selectbox("Material type:", ("None","Metallic","Composite","Polymer","Ceramic","Other"))
        material_type_option = other_textbox(material_type_option, "material type", key="material_other")

        input_load_type = st.text_input("Input (Load) Magnitude in SI Units:", placeholder="Enter Magnitude")
        load_type_option = st.selectbox("Load Type:", ("None","Force (kN)", "Pressure (MPa)", "Energy (J)", "Displacement (mm)", "Velocity (m/s)", "Acceleration (m/s^2)", "Other"))
        load_type_option = other_textbox(load_type_option, "load type", key="load_other")

        trial_input = st.number_input("Trial #:", min_value=0, step=1, placeholder="Enter trial number...")

    # Directory name variable and writes the directory name in the  bottom of the program
    if facility_type_sub_option == "UNDEX":
        directory_name = f"{username_textbox}/{facility_type_main_option}/{facility_type_sub_option}/{username_textbox}-{material_type_option}-{charge_type}-{Date_form}-Trial-{trial_input}"

    else:
        directory_name = f"{username_textbox}/{facility_type_main_option}/{facility_type_sub_option}/{username_textbox}-{material_type_option}-{input_load_type}-{Date_form}-Trial-{trial_input}"
    st.write("Directory:", directory_name)

    if st.button("Create Directory"):
        # Validate required fields
        if not username_textbox:
            st.error("Please enter your name.")
        elif facility_type_main_option == "None":
            st.error("Please select a facility type.")
        elif facility_type_sub_option == "":
            st.error("Please select an experiment type.")
        elif material_type_option == "None":
            st.error("Please select a material type.")
        elif not input_load_type:
            st.error("Please enter the input load magnitude.")
        elif load_type_option == "None":
            st.error("Please select a load type.")
        elif trial_input == 0:
            st.error("Please enter a trial number.")
        else:
            # Combine NAS path with folder name to create full path
            full_path = os.path.join(nas_path, directory_name)

            # Checks if the directory already exists
            if os.path.exists(full_path):
                st.error(f"Directory '{full_path}' already exists. Please choose a different name.")
            else:
                try:
                    # Creates the directory if it doesn't exist
                    os.makedirs(full_path, exist_ok=True)
                    st.success(f"Directory '{directory_name}' created successfully at '{full_path}'")
                except OSError as e:
                    st.error(f"Failed to create directory: {e}")