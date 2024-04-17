import curses 
from curses import wrapper
import time
import requests

def get_random_words(num_words=6):
    response = requests.get(f"https://random-word-api.herokuapp.com/word?number={num_words}")
    if response.status_code == 200:
        return ' '.join(response.json())
    else:
        return "Error fetching words"
    
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Test your WPM")
    stdscr.addstr("\nPress any key to start")
    stdscr.refresh()
    stdscr.getkey()

def display(stdscr, target_text, current_text, wpm = 0):
    
    stdscr.addstr(target_text)
    stdscr.addstr(1,0,f"WMP: {wpm:,.0f}")
    for i, char in enumerate (current_text):

        #determine the color of the text. If they match, green else red.
        color = curses.color_pair(2 if char != target_text[i] else 1)
        #starting on the same row, but on the character of interest
        stdscr.addstr(0,i, char,color)

def wpm_test(stdscr):
    target_text = get_random_words(10)
    current_text = []

    start_time = time.time()
    stdscr.nodelay(True)
    while True:
        cur_time = max(time.time() - start_time,1)
        # Avoid division by zero and better calculation of WPM:
        # Calculate words typed as len(current_text) / 5 (standard word length)
        # Divide by the minutes passed
        wpm = (len(current_text) / 5) / (cur_time / 60) if cur_time > 0 else 0

        stdscr.clear()
        
        display(stdscr, target_text, current_text, wpm)

        stdscr.refresh()
        try:
            key= stdscr.getkey()
        except:
            continue
        if ord(key) ==27:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text)> 0:
                current_text.pop()
        elif len(current_text) < len(target_text) - 1:    
            current_text.append(key)

        else:
            break
    
    print(f"You did it!\nYour wpm is: {wpm:.0f}")

#outputting to a new screen 
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #the integer of 1 represents the pair green and white
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) 
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) 
    start_screen(stdscr)
    wpm_test(stdscr)
# it will restore the state of your terminal if any error occurs during the execution
wrapper(main)