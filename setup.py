from cx_Freeze import setup, Executable

# Define the wrapper script
def main():
    import subprocess
    import sys
    subprocess.run(["streamlit", "run", "your_app.py"])

# Setup configuration
setup(
    name="YourApp",
    version="0.1",
    description="Description of your app",
    executables=[Executable("run_streamlit.py", base=None)]
)
