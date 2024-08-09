import streamlit as st
import datetime
import os
from back_end.drive_manager import get_available_drives
from back_end.directory_manager import create_directory, directory_exists

def render_create_tab():
    def other_textbox(selected_option, label, key):
        if selected_option == "Other":
            selected_option = st.text_input(f"Specify {label}:", key=key)
        return selected_option

    st.header("Dynamic Photomechanics Laboratory")
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

    facility_type_main_option = st.selectbox("Facility Type:", list(facility_options.keys()))
    sub_options = facility_options.get(facility_type_main_option, [""])

    if facility_type_main_option == "Other":
        facility_type_main_option = st.text_input("Please type facility type:", key="facility_main_other")
        facility_type_sub_option = st.text_input("Please type experiment type:", key="facility_sub_other")
    else:
        facility_type_sub_option = st.selectbox(
            f"Experiment type for {facility_type_main_option}:",
            sub_options
        )
        facility_type_sub_option = other_textbox(facility_type_sub_option, "experiment type", key="facility_sub_other")

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
        load_type_array = {
            "None": [],
            "Force (kN)": ["kN"],
            "Pressure (MPa)": ["MPa"],
            "Energy (J)": ["J"],
            "Displacement (mm)": ["mm"],
            "Velocity (ms^-1)": ["ms^-1"],
            "Acceleration (ms^-2)": ["ms^-2"],
            "Other": [""],
        }
        load_type_options = st.selectbox("Load type:", list(load_type_array.keys()))
        other_type_option = st.text_input("Please type load type", key="load_other") if load_type_options == "Other" else ""
        trial_input = st.number_input("Trial #:", min_value=0, step=1, placeholder="Enter trial number...")
        load_type_unit = other_type_option if load_type_options == "Other" else load_type_array[load_type_options][0] if load_type_array[load_type_options] else ""

    available_drives = get_available_drives()
    drive_labels = [f"{letter} ({label})" for letter, label in available_drives]
    selected_drive_index = st.selectbox("Select a Drive:", range(len(drive_labels)), format_func=lambda x: drive_labels[x])
    selected_drive = available_drives[selected_drive_index][0]

    st.session_state.user_directory_path = os.path.join(selected_drive, username_textbox)

    if facility_type_sub_option == "UNDEX":
        directory_name = f"{username_textbox}/{facility_type_main_option}/{facility_type_sub_option}/{username_textbox}-{material_type_option}-{charge_type}-{Date_form}-Trial-{trial_input}"
    else:
        directory_name = f"{username_textbox}/{facility_type_main_option}/{facility_type_sub_option}/{username_textbox}-{material_type_option}-{input_load_type}{load_type_unit}-{Date_form}-Trial-{trial_input}"

    st.write("Directory:", directory_name)

    if 'created_directory_path' not in st.session_state:
        st.session_state.created_directory_path = ""

    if st.button("Create", key="create_directory"):
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
            full_path = os.path.join(st.session_state.user_directory_path, directory_name)
            success, message = create_directory(full_path)
            if success:
                st.success(message)
                st.session_state.created_directory_path = full_path
            else:
                st.error(message)

    if st.session_state.created_directory_path:
        if st.button("Open Directory", key="open_directory"):
            try:
                if directory_exists(st.session_state.created_directory_path):
                    os.startfile(st.session_state.created_directory_path)
                else:
                    st.error("The directory does not exist.")
            except Exception as e:
                st.error(f"Failed to open directory: {e}")
