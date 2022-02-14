import curses 
from curses import wrapper
import random
import time
from os import system

system('mode con: cols=110 lines=25')

def start_screen(stdscr):
    stdscr.clear() # Clears the screen
    stdscr.addstr("Welcome to the Speed Typing Test!") # Display welcome text
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh() # Show what has been added before
    stdscr.getkey() # If a key is pressed it exits the function
    
    
        
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target) # Displays text sent through a variable
    stdscr.addstr(5, 0, f"WPM: {wpm}") # Shows WPM

    for i, char in enumerate(current): # Checking if the letters are correct or false
        correct_char = target[i] # Takes the correct character from the target sent through a variable
        color = curses.color_pair(1) # Default text is set to be a color set in main function
        if char != correct_char: # Checks if letters are correct
            color = curses.color_pair(2) # If letter isn't correct it changes the text color defined in main function
        stdscr.addstr(0, i, char, color) # Writes the key written
      
def load_text():
    with open('text.txt', 'r') as f: # Opens the txt file in R mode
        lines = f.readlines() # Reads all the lines in the file
        return random.choice(lines).strip() # Randomizes lines and takes the one assigned as first
            
def wpm_test(stdscr):
    target_text = load_text() # Takes the text from load_text function
    current_text = [] # Adds the text you type into an array
    wpm = 0 # Gives a default number to WPM(Words per minute)
    start_time = time.time() # Gives a start time
    stdscr.nodelay(True) # Added so the WPM keeps going even if keys aren't pressed which it work in realtime
    
    while True:
        ############################
        #    Logic to get the WPM in correct timing
        time_elapsed = max(time.time() - start_time, 1) 
        wpm = round((len(current_text) / (time_elapsed / 60)) /5)
        ############################
        
        stdscr.clear() # Clears the terminal

        display_text(stdscr, target_text, current_text, wpm) # Sends parameters to the display_text function

        stdscr.refresh() # Refreshes and shows the function called before
        
        if "".join(current_text) == target_text: # Converts the written text into a string
            stdscr.nodelay(False) # Stops the count so it shows your WPM
            break # Stops the program and sends you to the next function
        ############################
        #         Added so it doesn't crash if a key isn't pressed
        try:
            key = stdscr.getkey()
        except:
            continue
        ############################ 
        if ord(key) == 27: # Key number 27 is escape(ESC)
            break # If such key is pressed the function ends
        
        
        if key in ("KEY_BACKSPACE", '\b', "\x7f"): # Checks for backspace, multiple parameters because every OS uses different way to check the key
            if len(current_text) > 0: # Checking if the written text is longer than 0
                current_text.pop() # If the written text is longer than 0 and then if clicked backspace it deletes the character
        elif len(current_text) < len(target_text): # If the string is empty
            current_text.append(key) 

def main(stdscr):
    ############################
    #     Given variables to be used globally throughout the functions to change text color
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    ############################
    start_screen(stdscr) # Calls up the start_screen function
    while True:
        wpm_test(stdscr) # Calls up the wpm_test function
        
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...") # When the wpm_test function ends it shows the given string 
        key = stdscr.getkey() # Gets the key pressed
        if ord(key) == 27: # If escape is pressed
            break # The function ends
    
wrapper(main) # Shows up the main function which contains all the logic/functions