import sys
import threading
from automation import start_automation

def run_terminal():
    print("\n--- Terminal Configuration Mode ---")
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    chat_url = input("Enter Target Chat URL: ")
    message = input("Enter Message Text: ")
    try:
        interval = float(input("Enter Interval Delay (seconds) [Default 30]: ") or 30)
    except ValueError:
        interval = 30.0
        
    print("\nStarting background task. Press Ctrl+C to abort.")
    stop_event = threading.Event()
    try:
        start_automation(username, password, chat_url, message, interval, stop_event, print)
    except KeyboardInterrupt:
        stop_event.set()
        print("\nTerminal loop termination intercepted.")

def main():
    print("========================================")
    print("         Instabot Spammer Engine        ")
    print("========================================")
    print("[0] Run in Terminal Mode")
    print("[1] Run in Graphical Mode (GUI)")
    print("========================================")
    
    choice = input("Select operation mode (0 or 1): ").strip()
    
    if choice == "0":
        run_terminal()
    elif choice == "1":
        try:
            from gui_mode import launch_gui
            launch_gui()
        except ImportError as e:
            print(f"GUI engine load crash: {e}. Defaulting to CLI layout.")
            run_terminal()
    else:
        print("Invalid operational flag definition.")

if __name__ == "__main__":
    main()
