import ctypes
from src.gui import FileEncryptorGUI

def main():
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = FileEncryptorGUI()
    app.run()

if __name__ == "__main__":
    main() 
