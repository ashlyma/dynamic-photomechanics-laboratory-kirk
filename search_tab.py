import streamlit as st
import os
from back_end.drive_manager import get_available_drives

def render_search_tab():
    st.header("Search Files and Folders")

    # Get available drives
    available_drives = get_available_drives()
    drive_labels = [f"{letter} ({label})" for letter, label in available_drives]

    # Allow user to select a drive
    selected_drive_index = st.selectbox("Select a Drive:", range(len(drive_labels)), format_func=lambda x: drive_labels[x], key = "search_tab_select_drive_option")
    selected_drive = available_drives[selected_drive_index][0]

    # Set current path to the selected drive
    st.session_state.current_path = selected_drive
    
    if st.session_state.current_path:
        st.write(f"Current Search Path: {st.session_state.current_path}")
    else:
        st.warning("Please select a drive to search.")

    search_query = st.text_input("Enter file or folder name:")

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
            st.error("Please select a drive before searching.")
