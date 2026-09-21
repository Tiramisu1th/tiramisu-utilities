import pydirectinput
import time

def auto_clicker():
    print("Auto-clicker started. Clicking every 29 seconds.")
    print("Press Ctrl+C in this console to stop.")
    
    try:
        while True:
            # Wait for exactly 29 seconds
            time.sleep(29)
            
            # Send a hardware-level left mouse click
            pydirectinput.click()
            print("Left clicked!")
            
    except KeyboardInterrupt:
        # Graceful exit when you press Ctrl+C
        print("\nAuto-clicker stopped.")

def ww3_edge():
    print("Starting in 3 seconds. Please switch to the Roblox window...")
    time.sleep(3)
    auto_clicker()
    
if __name__ == "__main__":
    ww3_edge()
    
