# Write to upper text box and press convert to see converion on lower text box
# Use dots and dashes to write morse code. Separate letters with space and words with | (pipe)
import tkinter as tk
from turtle import title
from playsound import playsound #May have to <pip install playsound==1.2.2>
from PIL import ImageTk, Image

# Root window
root = tk.Tk()
root.title('Morse Code')
root.iconbitmap('icons/antenna.ico')
root.geometry('650x600+400+100')
root.resizable(0,0)

# Fonts and colors
button_font = ('helvetica', 12)
root_color = 'black'
frame_color = 'lightgrey'
button_color = 'lightgrey'
button_text_color = 'black'
box_text_color = 'white'
box_text_font = ('helvetica', 12)
root.config(bg=root_color)

# Functions
def convert():
    """Conversion based on radio button selected"""

    if language.get() == 1:
        get_morse()
    elif language.get() == 2:
        get_english()

def get_morse():
    """Converting to Morse"""

    morse_code = ""

    text = input_text.get("1.0", tk.END)
    text = text.lower()

    # Remove letter if not in dictionary
    for letter in text:
        if letter not in english_to_morse.keys():
            text = text.replace(letter, '')

    # Break up to words based on space and put into list
    word_list = text.split(" ")

    # List of letters
    for word in word_list:
        letters = list(word)
        # Get the correct morse and append to morse_code string
        for letter in letters:
            morse_char = english_to_morse[letter]
            morse_code += morse_char
            morse_code += " "
        # Separate words with |
        morse_code += "| "

    output_text.insert("1.0", morse_code)

def get_english():
    """Converting to English"""

    english = ""

    text = input_text.get("1.0", tk.END)

    # Remove if not in dictionary
    for m_letter in text:
        if m_letter not in morse_to_english.keys():
            text = text.replace(m_letter, '')

    # Break up to words based on | and put into list
    word_list = text.split("|")

    # Words into list of morse letters
    for word in word_list:
        letters = word.split(" ")
        # Get the correct letter and append it to english string
        for m_letter in letters:
            english_char = morse_to_english[m_letter]
            english += english_char
        # Separate words
        english += " "
    
    output_text.insert("1.0", english)

def clear():
    """Clear text boxes"""

    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

def play():
    """Play morse tones"""

    # Where is morse code
    if language.get() == 1:
        text = output_text.get("1.0", tk.END)
    elif language.get() == 2:
        text = input_text.get("1.0", tk.END)

    # Play morse tones 
    for v in text:
        if v == ".":
            playsound("sounds/dot.mp3")
            root.after(100) #ms
        elif v == "-":
            playsound("sounds/dash.mp3")
            root.after(200)
        elif v == " ":
            root.after(300)
        elif v == "|":
            root.after(500)
        else:
            pass

def show_guide():
    """Show code guide in another window"""

    # Image and window needs to be global
    global morse
    global guide

    # Second window to the root window
    guide = tk.Toplevel()
    guide.title("Morse Guide")
    guide.iconbitmap("icons/antenna.ico")
    guide.geometry('400x400+1050+100')
    guide.config(bg=root_color)

    # Create image, label and pack
    morse = ImageTk.PhotoImage(Image.open("pictures/morse_chart.JPG"))
    label = tk.Label(guide, image=morse, bg=frame_color)
    label.pack(padx=10, pady=10, ipadx=5, ipady=5)

    # Close button
    close_button = tk.Button(guide, text="Close", font=button_font, bg=button_color, command=hide_guide)
    close_button.pack(padx=10, pady=(20,0), ipadx=50)

    # Disable guide button
    guide_button.config(state=tk.DISABLED)

def hide_guide():
    """Hide the guide window"""

    guide_button.config(state=tk.NORMAL)
    guide.destroy()
    
    
# Letter / morse code dictionaries
english_to_morse = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..',
                    'e': '.', 'f': '..-.', 'g': '--.', 'h': '....',
                    'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
                    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.',
                    'q': '--.-', 'r': '.-.', 's': '...', 't': '-',
                    'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
                    'y': '-.--', 'z': '--..', '1': '.----',
                    '2': '..---', '3': '...--', '4': '....-', '5': '.....',
                    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
                    '0': '-----', ' ':' ', '|':'|', "":"" }
        
morse_to_english = dict([(value, key) for key, value in english_to_morse.items()]) # Flips around keys and values

# Layout frames
input_frame = tk.LabelFrame(root, bg=frame_color)
output_frame = tk.LabelFrame(root, bg=frame_color)
input_frame.pack(padx=16, pady=(16,8))
output_frame.pack(padx=16, pady=(8,16))

# Input frame
input_text = tk.Text(input_frame, height=14, width=45, fg=box_text_color, font=box_text_font, bg=root_color, border=3, insertbackground='white')
input_text.grid(row=0, column=1, rowspan=3, padx=5, pady=5)

language = tk.IntVar()
language.set(1)
morse_button = tk.Radiobutton(input_frame, text="English --> Morse Code", variable=language, value=1, font=button_font, fg=button_text_color, bg=button_color)
english_button = tk.Radiobutton(input_frame, text="Morse Code --> English", variable=language, value=2, font=button_font, fg=button_text_color, bg=button_color)
guide_button = tk.Button(input_frame, text="Guide", font=button_font, fg=button_text_color, bg=button_color, border=3, command=show_guide)

morse_button.grid(row=0, column=0, pady=(15,0))
english_button.grid(row=1, column=0)
guide_button.grid(row=2, column=0, padx=10, sticky='WE')

# Output frame
output_text = tk.Text(output_frame, height=14, width=45, fg=box_text_color, font=box_text_font, bg=root_color, border=3)
output_text.grid(row=0, column=1, rowspan=4, padx=5, pady=5)

convert_button = tk.Button(output_frame, text="Convert", font=button_font, fg=button_text_color, bg=button_color, border=3, command=convert)
play_button = tk.Button(output_frame, text="Play Morse", font=button_font, fg=button_text_color, bg=button_color, border=3, command=play)
clear_button = tk.Button(output_frame, text="Clear", font=button_font, fg=button_text_color, bg=button_color, border=3, command=clear)
quit_button = tk.Button(output_frame, text="Quit", font=button_font, fg=button_text_color, bg=button_color, border=3, command=root.destroy)

convert_button.grid(row=0, column=0, padx=10, ipadx=52) # Internal padding now defines column width
play_button.grid(row=1, column=0, padx=10, sticky='WE') # And stick to that column width with WEST and EAST
clear_button.grid(row=2, column=0, padx=10, sticky='WE')
quit_button.grid(row=3, column=0, padx=10, sticky='WE')

# Run root window
root.mainloop()