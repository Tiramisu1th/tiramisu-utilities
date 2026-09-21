import pydirectinput
import time
import random

def prevent_afk():
    print("AFK prevention started. Press Ctrl+C in this console to stop.")
    
    try:
        while True:
            # Send the hardware-level spacebar press to Roblox
            pydirectinput.press('space')
            print("Jumped to prevent AFK kick!")
            
            # Wait for a random interval between 5 and 10 minutes (300 to 600 seconds)
            wait_time = random.randint(300, 600) 
            
            minutes = wait_time // 60
            seconds = wait_time % 60
            print(f"Waiting for {minutes} minutes and {seconds} seconds before the next jump...")
            
            time.sleep(wait_time)
            
            
    except KeyboardInterrupt:
        # Graceful exit when you press Ctrl+C
        print("\nAFK prevention stopped.")

def roblox_anti_afk():
    print("Starting in 1 second. Please switch to the Roblox window...")
    time.sleep(1)
    pydirectinput.press('space')
    print("Making another hop between 2-5 seconds... as confirmation that the script is running.")
    time.sleep(random.randint(2, 5))
    prevent_afk()
    
if __name__ == "__main__":
    roblox_anti_afk()