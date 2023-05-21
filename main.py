import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import csv
import time

"""
Header where 000000XX is the number of defined items + 0x05 (total asm lines)
C20C9968 00000023
9421FFF0 7C0802A6
90010014 93E10000
48000079

is the following asm

stwu r1, -16(r1)
mflr r0
stw r0, 20(r1)
stw r31, 0(r1)
li r3, 0x2A
lis r4, 0x8003
ori r4, r4, 0xB0CC
mtctr r4
bctrl

"""

gecko_code_header = f"""
C20C9968 00000024
9421FFF0 7C0802A6
90010014 93E10000
4800007D 60000000 
"""

gecko_code_footer = f"""
7CE802A6 38E70004
38600000 38800000
2C030074 41820014
7CA71A2E 7C842A14
38630004 4BFFFFEC
3CA08003 60A5B0CC
7CA903A6 7C832378
4E800421 38800000
38A00000 2C050074
41820024 7CC72A2E
7C661850 2C030000
40A00008 48000010
38840001 38A50004
4BFFFFDC 1C840004
38840002 7C67222E
83E10000 80010014
7C0803A6 38210010
4E800020 00000000
"""

button_vars = []
entry_boxes = []
check_buttons = []

button_texts = {
    "Super Mushroom": "1",    # 00000001
    "Cursed Mushroom": "2",   # 00000002
    "Warp Pipe": "3",         # 00000003
    "Klepto": "4",            # 00000004
    "Bubble": "5",            # 00000005
    "Wiggler": "6",           # 00000006
    "Hammer Bro": "A",        # 0000000A
    "Coin Block": "B",        # 0000000B
    "Spiny": "C",             # 0000000C
    "Paratroopa": "D",        # 0000000D
    "Bullet Bill": "E",       # 0000000E
    "Goomba": "F",            # 0000000F
    "Bob-omb": "10",          # 00000010
    "Koopa Bank": "11",       # 00000011
    "Kamek": "14",            # 00000014
    "Mr. Blizzard": "15",     # 00000015
    "Piranha Plant": "16",    # 00000016
    "Magikoopa": "17",        # 00000017
    "Ukiki": "18",            # 00000018
    "Lakitu": "19",           # 00000019
    "Tweester": "1E",         # 0000001E
    "Duel": "1F",             # 0000001F
    "Chain Chomp": "20",      # 00000020
    "Bone": "21",             # 00000021
    "Bowser": "22",           # 00000022
    "Chance": "23",           # 00000023
    "Miracle": "24",          # 00000024
    "Donkey Kong": "25",      # 00000025
    "Versus": "26"            # 00000026
}

def clear_selections():
    for i, var in enumerate(button_vars):
        entry_boxes[i].delete(0, tk.END)
        entry_boxes[i].insert(0, '0')
        var.set(0)

def set_button_and_entry(index, weight, checked):
    button_vars[index].set(checked)
    entry_boxes[index].delete(0, tk.END)
    entry_boxes[index].insert(0, str(weight))
    if checked == 0:
        check_buttons[index].config(fg='grey')
    else:
        check_buttons[index].config(fg='black')

def save_csv():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])

    if file_path:
        button_text_keys = list(button_texts.keys())
        with open(file_path, 'w', newline='') as file:
            fieldnames = ['name', 'weight', 'on/off']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(button_text_keys)):
                name = button_text_keys[i]
                weight = int(entry_boxes[i].get())
                checked = button_vars[i].get()

                writer.writerow({'name': name, 'weight': weight, 'on/off': checked})

def load_csv():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        clear_selections()
        button_text_keys = list(button_texts.keys())
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                name = row['name']
                weight = int(row['weight'])
                checked = int(row['on/off'])
                if name in button_text_keys:
                    i = button_text_keys.index(name)
                    set_button_and_entry(i, weight, checked)
                    on_checkbutton_change(i)  # Update checkbox color


def on_button_click(button_number):
    print(button_texts[button_number - 1] + " checked!")

def generate_gecko_code():
    button_text_keys = list(button_texts.keys())
    code_str = ""

    for i in range(len(button_text_keys)):
        current_weight = int(entry_boxes[i].get())
        # Add weight as a 2-byte hexadecimal
        weight_hex = format(current_weight, '04x')
        # Add item id
        item_id = format(int(button_texts[button_text_keys[i]], 16), '04x')
        # Append to the code string
        code_str += weight_hex + item_id

        # Add a newline character after odd iterations, and a space after even iterations
        if (i+1) % 2 == 0:
            code_str += "\n"
        else:
            code_str += " "
    
    print("\n" + gecko_code_header + code_str + "00000000" + gecko_code_footer)

def on_generate_code():
    no_weight = 0
    checked_weights = 0
    total_weights = 0
    os.system('cls')  # Clear console for Windows
    time.sleep(0.05)  # Pause for 0.2 seconds
    button_text_keys = list(button_texts.keys())
    for i, var in enumerate(button_vars):
        current_weight = int(entry_boxes[i].get())
        if check_buttons[i].cget('fg') == 'grey':
            continue
        total_weights += current_weight
        if var.get() == 1:
            if current_weight == 0:
                no_weight = 1
                print(f"{button_text_keys[i]} has no weight!")
            else:
                checked_weights += current_weight
    if total_weights == 0:
        print("Weight Total was 0!")
        return
    if no_weight == 1:
        print("All selected items must have weights!")
        return
    for i, var in enumerate(button_vars):
        if check_buttons[i].cget('fg') == 'grey':
            continue
        current_weight = int(entry_boxes[i].get())
        if current_weight == 0:
            continue
        item_name = button_text_keys[i]  # Get the name of the checked item
        item_percentage = (current_weight / total_weights) * 100
        if item_percentage != 0:
            print(f'{item_name}: {item_percentage:.2f}%')

    checked_buttons = [i+1 for i, var in enumerate(button_vars) if var.get() == 1]

    if not checked_buttons:
        return
    generate_gecko_code()


def on_checkbutton_change(index):
    if button_vars[index].get() == 0:
        entry_boxes[index].delete(0, tk.END)
        entry_boxes[index].insert(0, "0")
        check_buttons[index].config(fg='grey') # Set the color to a lighter one when not checked
    else:
        check_buttons[index].config(fg='black') # Set the color to a darker one when checked

def open_help_window():
    help_window = tk.Toplevel()
    help_window.title("Help")
    help_window.geometry("300x200")

    #TODO fill in help text
    help_text = "This is the help text.\n\nYou can provide instructions or information here."
    help_label = tk.Label(help_window, text=help_text)
    help_label.pack()

def limit_size(P):
    if len(P) > 3: 
        return False
    if len(P) < 1: # Allow empty entries
        return True
    if P.isdigit() and 0 <= int(P) <= 999: # Check for a valid integer within the range
        return True
    else:
        return False

def clear_options():
    clear_selections()
    for i, var in enumerate(button_vars):
        check_buttons[i].config(fg='grey')

def create_gui():
    global button_vars
    global entry_boxes

    root = tk.Tk()
    root.title("Mario Party 5 Capsule Pool Gen")
    root.iconbitmap("Miracle_Capsule.ico")

    save_button = tk.Button(root, text="Save CSV", command=save_csv)
    save_button.pack()

    load_button = tk.Button(root, text="Load CSV", command=load_csv)
    load_button.pack()

    load_button = tk.Button(root, text="Clear All", command=clear_options)
    load_button.pack()

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab = tk.Frame(notebook)
    notebook.add(tab, text="PAL")

    num_rows = 10  # Number of rows
    num_columns = 3  # Number of columns

    for i in range(num_rows):
        for j in range(num_columns):
            index = i * num_columns + j
            button_text_keys = list(button_texts.keys())

            if index < len(button_texts):
                var = tk.IntVar()
                button_vars.append(var)
                entry_var = tk.StringVar()
                entry_var.set('0')  # Set default value to "0"
                # Registering validation command
                vcmd = root.register(limit_size)

                entry = tk.Entry(tab, width=4, textvariable=entry_var, validate='key', validatecommand=(vcmd, '%P'))
                entry_boxes.append(entry)

                checkbutton = tk.Checkbutton(tab, text=button_text_keys[index], variable=var, fg='grey', command=lambda i=index: on_checkbutton_change(i))
                check_buttons.append(checkbutton)  # Store the check button

                entry.grid(row=i, column=j*2, padx=5, pady=5, sticky="e")
                checkbutton.grid(row=i, column=j*2+1, padx=5, pady=5, sticky="w")

    generate_button = tk.Button(root, text="Generate Gecko Code", command=on_generate_code)
    generate_button.pack()

    help_button = tk.Button(root, text="Help", command=open_help_window)
    help_button.pack()

    root.mainloop()

def validate_input(value):
    if len(value) > 3:  # Limit input to 3 characters
        return False
    if not value.isdigit():  # Only allow numeric input
        return False
    return True

if __name__ == "__main__":
    create_gui()