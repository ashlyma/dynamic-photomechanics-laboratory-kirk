from cx_Freeze import setup, Executable

setup(
    name="NAS Lab",
    version="0.1",
    description="Description of your app",
    options={
        'build_exe': {
            'packages': ['streamlit'],
            'include_files': [('script.py', '.')]  # Include your app script in the build
        }
    },
    executables=[Executable("run_streamlit.py", base="Win32GUI")]
)
