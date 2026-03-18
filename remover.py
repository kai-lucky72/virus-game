import os
import winreg
import shutil

def remove_persistence():
    print("--- RCA Neural Strike Cleanup Tool ---")
    
    # 1. Remove Registry Key
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "NeuralStrike")
        winreg.CloseKey(key)
        print("[+] Registry persistence removed.")
    except Exception as e:
        print(f"[-] Registry key not found or error: {e}")

    # 2. Remove AppData Files
    try:
        app_data = os.environ.get("APPDATA")
        dest_folder = os.path.join(app_data, "DinoGame")
        if os.path.exists(dest_folder):
            shutil.rmtree(dest_folder)
            print("[+] AppData backoff files deleted.")
        else:
            print("[!] AppData folder already clean.")
    except Exception as e:
        print(f"[-] Error deleting files: {e}")

    print("\nCleanup Complete. System is now clean.")
    input("\nPress ENTER to exit...")

if __name__ == "__main__":
    remove_persistence()
