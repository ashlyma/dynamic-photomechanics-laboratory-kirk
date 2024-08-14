import streamlit as st
from back_end.search_engine import index_files, search_files
import os
from back_end.drive_manager import get_available_drives
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT

# Ensure the index directory and schema are set up
INDEX_DIR = "indexdir"

# Define the schema for Whoosh
schema = Schema(title=TEXT(stored=True), content=TEXT)

# Create or open the index
def initialize_index():
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        return create_in(INDEX_DIR, schema)
    else:
        return open_dir(INDEX_DIR)

def render_search_tab():
    st.header("Search Files and Folders")

    # Get available drives
    available_drives = get_available_drives()
    drive_labels = [f"{letter} ({label})" for letter, label in available_drives]

    # Allow user to select a drive
    selected_drive_index = st.selectbox("Select a Drive:", range(len(drive_labels)), format_func=lambda x: drive_labels[x], key="search_tab_select_drive_option")
    selected_drive = available_drives[selected_drive_index][0]

    # Set current path to the selected drive
    st.session_state.current_path = selected_drive
    
    if st.session_state.current_path:
        st.write(f"Current Search Path: {st.session_state.current_path}")
        
        # Initialize the index before attempting to use it
        ix = initialize_index()

        # Index files and folders when drive is selected
        if st.button("Index Drive"):
            st.write("Indexing files and folders...")
            try:
                index_files(ix, st.session_state.current_path)
                st.success("Indexing completed.")
            except Exception as e:
                st.error(f"Error during indexing: {str(e)}")

    else:
        st.warning("Please select a drive to search.")

    # Search query input
    search_query = st.text_input("Enter file or folder name:")

    # Execute the search when the search button is clicked
    if st.button("Search", key="search"):
        if st.session_state.current_path:
            try:
                # Ensure the index is opened properly before searching
                ix = open_dir(INDEX_DIR)
                results = search_files(ix, search_query)

                # Display search results
                if len(results) > 0:
                    st.write(f"Found {len(results)} results:")
                    for result in results:
                        st.write(result['title'])
                else:
                    st.write("No matching files or folders found.")
            except Exception as e:
                st.error(f"Error during search: {str(e)}")
        else:
            st.error("Please select a drive before searching.")
