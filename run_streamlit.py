# run_streamlit.py
import subprocess
import sys
import os

if __name__ == "__main__":
    # Ensure the script path is correct
    script_path = os.path.abspath("script.py")

    # Run the Streamlit command
    subprocess.Popen(["streamlit", "run", script_path], creationflags=subprocess.CREATE_NO_WINDOW)
