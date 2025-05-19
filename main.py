import ctypes
from src.gui import FileEncryptorGUI
import os
import requests

def main():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    # Check if the icon file exists in src directory
    icon_path = os.path.join('src', 'lock_icon.png')
    if not os.path.exists(icon_path):
        print("Downloading icon file...")
        try:
            # GitHub raw content URL for the image
            github_url = "https://raw.githubusercontent.com/username/repo/main/lock_icon.png"
            response = requests.get(github_url)
            
            # Ensure src directory exists
            os.makedirs('src', exist_ok=True)
            
            # Save the image
            with open(icon_path, 'wb') as f:
                f.write(response.content)
            print("Icon downloaded successfully")
        except Exception as e:
            print(f"Failed to download icon: {e}")
    
    app = FileEncryptorGUI()
    app.run()

if __name__ == "__main__":
    main() 