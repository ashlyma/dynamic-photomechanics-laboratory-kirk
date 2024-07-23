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
    
    input_load_type = ""  # Initialize input_load_type to avoid NameError
    load_type_option = ""

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

    # Facility sub options appear based on the facility selected
    load_type_array = {
    "None": [],
    "Force (kN)": ["kN"],
    "Pressure (MPa)": ["MPa"],
    "Energy (J)": ["J"],
    "Displacement (mm)": ["mm"],
    "Velocity (ms^-1)": ["ms^-1"],
    "Acceleration (ms^-2)": ["ms^-2"],
    "Other": [""],  # This might cause issues when accessing [0]
}

    # Select the load type from the dropdown
    load_type_options = st.selectbox("Load type:", list(load_type_array.keys()))
    # Capture the other load type if "Other" is selected
    other_type_option = st.text_input("Specify other load type", key="load_other") if load_type_options == "Other" else ""

    trial_input = st.number_input("Trial #:", min_value=0, step=1, placeholder="Enter trial number...")

    # Extract the unit of the load type or use the other type option
    if load_type_options == "Other":
        load_type_unit = other_type_option
    else:
        load_type_unit = load_type_array[load_type_options][0] if load_type_array[load_type_options] else ""

    # Directory name variable and writes the directory name in the bottom of the program
    if facility_type_sub_option == "UNDEX":
        directory_name = f"{username_textbox}/{facility_type_main_option}/{facility_type_sub_option}/{username_textbox}-{material_type_option}-{charge_type}-{Date_form}-Trial-{trial_input}"
    else:
        directory_name = f"{username_textbox}/{facility_type_main_option}/{facility_type_sub_option}/{username_textbox}-{material_type_option}-{input_load_type}{load_type_unit}-{Date_form}-Trial-{trial_input}"

    # Display the directory name
    st.write("Directory:", directory_name)

    if st.button("Create"):
        # Validate required fields
        if not username_textbox:
            st.error("Please enter your name.")
        elif facility_type_main_option == "None":
            st.error("Please select a facility type.")
        elif facility_type_sub_option == "":
            st.error("Please select an experiment type.")
        elif material_type_option == "None":
            st.error("Please select a material type.")
        elif not input_load_type and not charge_type:
            st.error("Please enter load magnitude or the charge type.")
        elif load_type_option == "None"and not charge_type:
            st.error("Please select a load type or charge type.")
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


# Content under the tab 2 (Search)
with tab2:
    st.header("SearchD PML_Projects")

    # Initialize session state for current path
    if 'current_path' not in st.session_state:
        st.session_state.current_path = nas_path

    # Get current path from session state
    current_path = st.session_state.current_path

    # Search bar with a search button
    search_query = st.text_input("Search for files or directories:", "")
    search_button = st.button("Search")

    # Breadcrumb navigation
    st.write("Current path:", current_path)
    if current_path != nas_path:
        if st.button("Back"):
            # Move to parent directory
            st.session_state.current_path = os.path.dirname(current_path)
            current_path = st.session_state.current_path

    # Display contents of the current directory
    try:
        items = os.listdir(current_path)
        items.insert(0, "..")  # Option to go back to parent directory

        # Filter items based on search query if the search button is pressed
        if search_button and search_query:
            items = [item for item in items if search_query.lower() in item.lower()]

        if items:
            for item in items:
                item_path = os.path.join(current_path, item)
                display_name = f"📁 {item}" if os.path.isdir(item_path) else f"📄 {item}"
                if st.button(display_name):
                    if item == "..":
                        # Move to parent directory
                        st.session_state.current_path = os.path.dirname(current_path)
                        current_path = st.session_state.current_path
                    elif os.path.isdir(item_path):
                        # Move into the selected directory
                        st.session_state.current_path = item_path
                        current_path = st.session_state.current_path
                    else:
                        st.write(f"📄 {item}")
        else:
            st.write("No files or directories found.")
    except Exception as e:
        st.error(f"An error occurred while accessing the NAS path: {e}")
