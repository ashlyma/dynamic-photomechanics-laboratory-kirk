import streamlit as st
import os
import datetime
import win32api  # Make sure pywin32 is installed

# Function to get available drives with labels on Windows
def get_available_drives():
    drives = []
    for letter in win32api.GetLogicalDriveStrings().split('\000')[:-1]:  # Split the drive letters
        try:
            drive_label = win32api.GetVolumeInformation(letter)[0]  # Get the drive label
            drives.append((letter, drive_label))
        except Exception as e:
            drives.append((letter, "Unknown"))
    return drives

# Streamlit User Interface
tab1, tab2 = st.tabs(["Create", "Search"])

# Content under tab 1 (Home)
with tab1:
    def other_textbox(selected_option, label, key):
        if selected_option == "Other":
            selected_option = st.text_input(f"Specify {label}:", key=key)
        return selected_option

    # Title at the top of the page
    st.header("Dynamic Photomechanics Laboratory")

    # Username and date questions
    username_textbox = st.text_input("Name:", placeholder="Enter your first and last name...")
    Date_form = st.date_input("Experiment run-date:", value=datetime.datetime.now())

    # Facility options array
    facility_options = {
        "None": [],
        "Implosion Tank (aka 'Big' Tank)": ["Implosion", "UNDEX", "Other"],
        "Explosion Tank (aka 'Square' Tank)": ["UNDEX", "Other"],
        "Shock Tube (Gas)": ["AIREX", "Other"],
        "Hypersonic Shock Tube (Gas)": ["AIREX", "Other"],
        "Shock Tube (Water)": ["Air-backed Plate Shock", "Submerged UNDEX", "Other"],
        "Flyer Plate Impactor (Gas Gun)": ["Spalling", "Ballistic", "Other"],
        "SHPB (Dynamic)": ["Compression", "Tension", "Shear", "Fracture", "Other"],
        "Drop Weight tower (Dynamic)": ["Plate Impact", "Three Point Bending", "Compression", "Other"],
        "HITS (Dynamic)": ["Puncture", "Compression", "Other"],
        "Dynamic Mechanical Analyzer (DMA)": ["Three Point Bending", "Cantilever", "Double Cantilever", "Compression", "Tension", "Other"],
        "UTM (Static)": ["Tension", "Compression", "Shear", "Three Point Bending", "Four Point Bending", "Peel", "Other"],
        "Other": [""],
    }

    # Facility type main option
    facility_type_main_option = st.selectbox("Facility Type:", list(facility_options.keys()))
    
    # Determine the sub-options based on the main option selected
    sub_options = facility_options.get(facility_type_main_option, [""])

    # If "Other" is selected for the facility type, display a text box instead of the experiment type select box
    if facility_type_main_option == "Other":
        facility_type_main_option = st.text_input("Please type facility type:", key="facility_main_other")
        facility_type_sub_option = st.text_input("Please type experiment type:", key="facility_sub_other")
    else:
        # Experiment type option also known as sub-options
        facility_type_sub_option = st.selectbox(
            f"Experiment type for {facility_type_main_option}:",
            sub_options
        )
        facility_type_sub_option = other_textbox(facility_type_sub_option, "experiment type", key="facility_sub_other")

    # Initialize variables
    charge_type = ""
    input_load_type = ""
    load_type_options = ""

    # Material, trial, input load, and load type questions
    if facility_type_sub_option == "UNDEX":
        material_type_option = st.selectbox("Material type:", ("None", "Metallic", "Composite", "Polymer", "Ceramic", "Other"))
        material_type_option = other_textbox(material_type_option, "material type", key="material_other")
        charge_type = st.selectbox("Charge type:", ("None", "RP87", "RP80", "RP501", "RP502", "RP503", "Other"))
        charge_type = other_textbox(charge_type, "charge type", key="charge_type_other")
        trial_input = st.number_input("Trial #:", min_value=0, step=1, placeholder="Enter trial number...")
    else:
        material_type_option = st.selectbox("Material type:", ("None", "Metallic", "Composite", "Polymer", "Ceramic", "Other"))
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
        other_type_option = st.text_input("Please type load type", key="load_other") if load_type_options == "Other" else ""

        trial_input = st.number_input("Trial #:", min_value=0, step=1, placeholder="Enter trial number...")

        # Extract the unit of the load type or use the other type option
        if load_type_options == "Other":
            load_type_unit = other_type_option
        else:
            load_type_unit = load_type_array[load_type_options][0] if load_type_array[load_type_options] else ""

    # Add the "Select Drive" dropdown
    available_drives = get_available_drives()
    drive_labels = [f"{letter} ({label})" for letter, label in available_drives]
    selected_drive_index = st.selectbox("Select a Drive:", range(len(drive_labels)), format_func=lambda x: drive_labels[x])
    selected_drive = available_drives[selected_drive_index][0]

    # Set the directory path
    st.session_state.user_directory_path = os.path.join(selected_drive, username_textbox)

    # Directory name variable and display the directory name and create button
    if facility_type_sub_option == "UNDEX":
        directory_name = f"{username_textbox}/{facility_type_main_option}/{facility_type_sub_option}/{username_textbox}-{material_type_option}-{charge_type}-{Date_form}-Trial-{trial_input}"
    else:
        directory_name = f"{username_textbox}/{facility_type_main_option}/{facility_type_sub_option}/{username_textbox}-{material_type_option}-{input_load_type}{load_type_unit}-{Date_form}-Trial-{trial_input}"

    # Display the directory name
    st.write("Directory:", directory_name)

    # Initialize session state variables to store the created directory path
    if 'created_directory_path' not in st.session_state:
        st.session_state.created_directory_path = ""

    if st.button("Create", key="create_directory"):
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
        elif load_type_options == "None" and not charge_type:
            st.error("Please select a load type or charge type.")
        elif trial_input == 0:
            st.error("Please enter a trial number.")
        else:
            # Combine selected drive path with folder name to create full path
            full_path = os.path.join(st.session_state.user_directory_path, directory_name)

            # Checks if the directory already exists
            if os.path.exists(full_path):
                st.error(f"Directory '{full_path}' already exists. Please choose a different name.")
            else:
                try:
                    # Creates the directory if it doesn't exist
                    os.makedirs(full_path, exist_ok=True)
                    st.success(f"Directory '{directory_name}' created successfully at '{full_path}'")

                    # Store the path of the created directory
                    st.session_state.created_directory_path = full_path
                except OSError as e:
                    st.error(f"Failed to create directory: {e}")

    # Display the "Open Directory" button if the directory was created
    if st.session_state.created_directory_path:
        # Create a button to open the directory
        if st.button("Open Directory", key="open_directory"):
            try:
                # Check if the directory exists before trying to open it
                if os.path.exists(st.session_state.created_directory_path):
                    # Open the directory in file explorer
                    os.startfile(st.session_state.created_directory_path)
                else:
                    st.error("The directory does not exist.")
            except Exception as e:
                st.error(f"Failed to open directory: {e}")

# Content under tab 2 (Search)
with tab2:
    st.header("Search Files and Folders")

    # Initialize session state for current path
    if 'current_path' not in st.session_state:
        if 'user_directory_path' in st.session_state:
            st.session_state.current_path = st.session_state.user_directory_path
        else:
            st.session_state.current_path = None

    # Display the current path to search within
    if st.session_state.current_path:
        st.write(f"Current Search Path: {st.session_state.current_path}")
    else:
        st.warning("Please create a directory in the 'Create' tab before searching.")

    # File or folder name input
    search_query = st.text_input("Enter file or folder name:")

    # Handle the search
    if st.button("Search", key="search"):
        if st.session_state.current_path:
            search_results = []
            for root, dirs, files in os.walk(st.session_state.current_path):
                for name in files + dirs:
                    if search_query.lower() in name.lower():
                        search_results.append(os.path.join(root, name))
            if search_results:
                st.write("Search Results:")
                for result in search_results:
                    st.write(result)
            else:
                st.write("No matching files or folders found.")
        else:
            st.error("Please create a directory before searching.")
