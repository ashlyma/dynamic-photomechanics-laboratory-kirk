import win32api

def get_available_drives():
    drives = []
    for letter in win32api.GetLogicalDriveStrings().split('\000')[:-1]:  # Split the drive letters
        try:
            drive_label = win32api.GetVolumeInformation(letter)[0]  # Get the drive label
            drives.append((letter, drive_label))
        except Exception as e:
            drives.append((letter, "Unknown"))
    return drives
