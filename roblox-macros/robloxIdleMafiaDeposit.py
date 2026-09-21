# Thanks Gemini for suggesting pydirectinput to help me to prevent AFK kick in Roblox.
import pydirectinput
import time 
import random

def gauss_wrapper(mu: float, sigma: float, min_value: float=0.0, max_value: float | None = None) -> float:
    """
    A wrapper for random.gauss that ensures the returned value is not less than min.
    """
    out: float = random.gauss(mu, sigma)
    if max_value is None:
        return max(out, min_value)
    elif min_value > max_value:
        raise ValueError("師兄啊, min_value cannot be greater than max_value")
    else:
        return max(min(out, max_value), min_value)

def deposit_coins():
    print("AFK prevention AND depositing coins started. Press Ctrl+C in this console to stop.")
    space_interval: int = 0
    deposit_interval: float = 0.0
    hold_duration: float = 0.0
    space_delay_interval: float = 0.0
    space_hold_interval: float = 0.0
    
    try:
        while True:
            # Random interval between 60-120 5-second intervals i.e. 5-10 minutes
            space_interval = random.randint(60,120)
            print(f"Depositing coins for the next {space_interval} cycles before jumping to prevent AFK kick...")
            # deposit loop that happens every ~5 seconds 
            for _ in range(space_interval):
                deposit_interval = gauss_wrapper(4.9, 0.1, 3) # sample a random clicking interval to prevent being too obvious
                time.sleep(deposit_interval)
                
                # Left-click to deposit coins. Note that I personally has around 6 CPS single-finger click, so assuming half of the time is holding and half time is lifted 
                hold_duration = gauss_wrapper(0.1, 0.01, 0.05, 0.15) # sample a random hold duration to prevent being too obvious
                pydirectinput.mouseDown(button='left')
                time.sleep(hold_duration)
                pydirectinput.mouseUp(button='left')
                
            # After the deposit loop, press the hardware-level spacebar to Roblox
            space_delay_interval = gauss_wrapper(0.9, 0.1, 0.1) # sample a random delay interval to prevent being too obvious
            time.sleep(space_delay_interval)
            space_hold_interval = gauss_wrapper(0.1, 0.01, 0.05, 0.15) # sample a random hold duration to prevent being too obvious
            pydirectinput.keyDown('space')
            time.sleep(space_hold_interval)
            pydirectinput.keyUp('space')
            print("Jumped to prevent AFK kick!")  
    except KeyboardInterrupt:
        # Graceful exit when you press Ctrl+C
        print("\nAFK prevention and coin depositing stopped.") 

def idle_mafia():
    print("Starting in 3 second. Please switch to the Roblox window...")
    time.sleep(3)
    pydirectinput.press('space')
    print("Making another hop between 2-5 seconds... as confirmation that the script is running.")
    time.sleep(random.randint(2, 5))
    pydirectinput.press('space')
    deposit_coins()
    
if __name__ == "__main__":
    idle_mafia()