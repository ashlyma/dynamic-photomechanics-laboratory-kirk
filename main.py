import streamlit as st
from front_end.create_tab import render_create_tab
from front_end.search_tab import render_search_tab

def main():
    st.set_page_config(page_title="Dynamic Photomechanics Laboratory", layout="wide")
    tab1, tab2 = st.tabs(["Create", "Search"])

    with tab1:
        render_create_tab()

    with tab2:
        render_search_tab()

if __name__ == "__main__":
    main()

