import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from gecko_code_dictionaries import *
from tkinter import filedialog
import csv
import os

frames = []
price_vars = []  # List to store price values
weight_vars = []  # List to store weight values
check_vars = []  # List to store check values
checkbuttons = []  # list to hold checkbutton widgets

def on_checkbutton_change(index):
    if check_vars[index].get():  # if checked
        checkbuttons[index].config(fg='black')
    else:  # if not checked
        checkbuttons[index].config(fg='grey')


def create_grid(frame, rows, columns, text_keys, text_items, current_tab):
    global price_vars
    global weight_vars
    global check_vars
    global checkbuttons
    price_vars = []  # List to store price values
    weight_vars = []  # List to store weight values
    check_vars = []  # List to store check values
    checkbuttons = []  # list to hold checkbutton widgets
    index = 0

    for r in range(rows):
        for c in range(columns):
            items_per_column = 3
            for i in range(items_per_column): #show items in rows of 3s
                if index >= len(text_keys):
                    return
                limit_coin_size_callback = frame.register(limit_coin_size)
                limit_weight_size_callback = frame.register(limit_weight_size)
                cur_row = rows * (r * columns + c)
                button_text, (price, weight, checked) = text_items[index]

                price_str_test = str(price)
                weight_str_test = str(weight)
                
                weight_icon = PhotoImage(file="ico/weight_icon_small_2.png")
                weight_icon_label = tk.Label(frame, image=weight_icon)
                weight_icon_label.image = weight_icon  # Keep a reference to the coin image
                weight_icon_label.grid(row=cur_row, column=i * items_per_column + 1, sticky="w")

                price_icon = PhotoImage(file="ico/price_icon_small_2.png")
                price_icon_label = tk.Label(frame, image=price_icon)
                price_icon_label.image = price_icon  # Keep a reference to the weight image
                price_icon_label.grid(row=cur_row, column=i * items_per_column, sticky="w")

                # Create Entry widgets for price box
                price_var = tk.StringVar(value=price_str_test)  # StringVar to store price value
                price_entry = tk.Entry(frame, width=3, textvariable=price_var, validate='key', validatecommand=(limit_coin_size_callback, '%P'))
                price_entry.grid(row=cur_row+1, column=i * items_per_column)
                price_vars.append(price_var)  # Store price_var in the list

                weight_var = tk.StringVar(value=weight_str_test)  # StringVar to store weight value
                weight_entry = tk.Entry(frame, width=3, textvariable=weight_var, validate='key', validatecommand=(limit_weight_size_callback, '%P'))
                weight_entry.grid(row=cur_row+1, column=i * items_per_column + 1)
                weight_vars.append(weight_var)  # Store weight_var in the list

                check_var = tk.BooleanVar(value=checked)
                
                if (check_var.get() == False):
                    checkbutton = tk.Checkbutton(frame, text=text_keys[index], variable=check_var, fg='grey', command=lambda index=index: on_checkbutton_change(index))
                else:
                    checkbutton = tk.Checkbutton(frame, text=text_keys[index], variable=check_var, fg='black', command=lambda index=index: on_checkbutton_change(index))
                checkbutton.grid(row=cur_row + 1, column=i * items_per_column + 2, sticky="w")
                check_vars.append(check_var)  # Store check_var in the list
                checkbuttons.append(checkbutton)  # Store checkbutton in the list

                index += 1


def tab_selected(event, tab_control):
    elements_per_row = 3
    max_num_of_columns = 10

    # Get the currently selected tab index
    current_tab = tab_control.index("current")
    #print(f"Current tab index{current_tab}")
    
    # Clear the frame before creating a new grid
    frame = frames[current_tab]
    for widget in frame.winfo_children():
        widget.destroy()

    button_text_keys = list(button_texts_list[current_tab].keys())
    button_text_items = list(button_texts_list[current_tab].items())
    create_grid(frame, elements_per_row, max_num_of_columns, button_text_keys, button_text_items, current_tab)


def limit_weight_size(P):
    if len(P) > 3: 
        return False
    if len(P) < 1: # Allow empty entries
        return True
    if P.isdigit() and 0 <= int(P) <= 999: # Check for a valid integer within the range
        return True
    else:
        return False

def limit_coin_size(P):
    if len(P) > 3: 
        return False
    if len(P) < 1: # Allow empty entries
        return True
    if P.isdigit() and 0 <= int(P) <= 255: # Check for a valid integer within the range
        return True
    else:
        return False


def open_help_window():
    help_window = tk.Toplevel()
    help_window.title("Help")
    help_window.geometry("300x200")
    help_text = "Mario Party 4/5/6 Item Pool Generator\nWritten by Rain"
    help_label = tk.Label(help_window, text=help_text)
    help_label.pack()


def clear_grid(tab_control):
    elements_per_row = 3
    max_num_of_columns = 10

    # Get the currently selected tab index
    current_tab = tab_control.index("current")
    #print(f"Current tab index{current_tab}")
    
    # Clear the frame before creating a new grid
    frame = frames[current_tab]
    for widget in frame.winfo_children():
        widget.destroy()

    button_text_keys = list(button_texts_list[current_tab].keys())
    button_text_items = list(button_texts_list[current_tab].items())
    create_grid(frame, elements_per_row, max_num_of_columns, button_text_keys, button_text_items, current_tab)


def create_file_menu(window, tab_control, version_var):
    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=lambda: clear_grid(tab_control))
    filemenu.add_command(label="Open", command=lambda: load_csv(tab_control, version_var))
    filemenu.add_command(label="Save", command=lambda: save_csv(tab_control, version_var))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About...", command=open_help_window)
    menubar.add_cascade(label="Help", menu=helpmenu)
    window.config(menu=menubar)
    

def create_version_buttons(window, version_var):
    # Create version radiobuttons
    version_frame = tk.Frame(window)
    version_frame.pack(side=tk.TOP)
    version_jp_button = tk.Radiobutton(window, text="JP", variable=version_var, value=0)
    version_jp_button.pack()
    version_us_button = tk.Radiobutton(window, text="US", variable=version_var, value=1)
    version_us_button.pack()
    version_pal_button = tk.Radiobutton(window, text="PAL", variable=version_var, value=2)
    version_pal_button.pack()


def on_generate_code(tab_control, version_var):
    verList = ["JP", "US", "PAL"]
    gameList = ["MP4", "MP5", "MP6"]

    #clear twice to avoid powershell leaving stuff in the window
    os.system('cls')  # Clear console for Windows
    os.system('cls')  # Clear console for Windows

    version = version_var.get()
    if version == 0: #is JP
        print("JP version not currently supported")
        return
    no_weight = 0
    checked_weights = 0
    total_weights = 0

    # Get the currently selected tab index
    current_tab = tab_control.index("current")
    button_text_keys = list(button_texts_list[current_tab].keys())
    button_text_items = list(button_texts_list[current_tab].items())
    total_weight = 0
    data_for_weight_gecko_code = ""
    data_for_price_gecko_code = ""
    gecko_code_game_header = gecko_code_headers[current_tab][version]
    gecko_code_game_footer = gecko_code_footers[current_tab][version]
    price_base_address = price_base_addresses[current_tab][version]
    item_names = list(item_names_and_ids_list[current_tab].keys())
    ids_items = list(item_names_and_ids_list[current_tab].items())
    price_gecko_code_string = ""
    lowest_price = 999 #max is 255 in tkinter program

    for i in range(len(button_text_items)):
        cur_item_weight = int(weight_vars[i].get())
        cur_item_price = int(price_vars[i].get())
        data_for_weight_gecko_code += hex(cur_item_weight)[2:].upper().zfill(4)
        data_for_weight_gecko_code += ids_items[i][1].upper().zfill(2)
        if current_tab == 0: #is mp4
            price_gecko_code_string += hex(int(price_base_address, 16) + int(ids_items[i][1], 16))[2:].upper().zfill(8)
            price_gecko_code_string += hex(cur_item_price)[2:].upper().zfill(8)
        elif current_tab == 1: #is mp5
            #multiply by 28 because it's the size of the capsule table struct
            #add 0x14 so base address points to struct member price
            price_gecko_code_string += hex(int(int(price_base_address, 16) + 0x14) + int(int(ids_items[i][1], 16) * 28))[2:].upper().zfill(8)
            price_gecko_code_string += hex(cur_item_price)[2:].upper().zfill(8)
        if check_vars[i].get() == 1:
            total_weight += cur_item_weight
            data_for_weight_gecko_code += hex(cur_item_price)[2:].upper().zfill(2)
            # Update lowest_price if the current item price is lower
            if cur_item_price < lowest_price:
                lowest_price = cur_item_price
        else:
            data_for_weight_gecko_code += "00" #set price to 00 if not checked

    if total_weight <= 0:
        print("Total weight was 0!")
        return

    print(f"Generating code for {gameList[current_tab]} {verList[version]}")
    print(f"The lowest item price is: {lowest_price}")

    

    for i in range(len(button_text_items)):
        cur_item_weight = int(weight_vars[i].get())
        item_percentage = (cur_item_weight / total_weight) * 100

        if item_percentage != 0:
            print(f'  {button_text_keys[i]}: {item_percentage:.2f}%')

    formatted_hex_string = ""

    if len(button_text_keys) % 2 == 1:
        #needed to fill the space in the gecko code which occurrs when an odd number of items are present
        data_for_weight_gecko_code = data_for_weight_gecko_code + "00000000" 


    # Insert spaces and new lines
    for i in range(0, len(data_for_weight_gecko_code), 8):
        chunk = data_for_weight_gecko_code[i:i+8]
        formatted_hex_string += chunk + " "
        if (i+8) % 16 == 0:
            formatted_hex_string += "\n"

    formatted_hex_string = formatted_hex_string.rstrip('\n')
    formatted_price_hex_string = ""

    if price_gecko_code_string != "":
        for i in range(0, len(price_gecko_code_string), 8):
            chunk = price_gecko_code_string[i:i+8]
            formatted_price_hex_string += chunk + " "
            if (i+8) % 16 == 0:
                formatted_price_hex_string += "\n"

    gecko_code_string = f"{gecko_code_game_header}{formatted_hex_string}{gecko_code_game_footer}{formatted_price_hex_string}"
    if (lowest_price) != -1:
        if (current_tab == 2): #is mp6 
            lowest_price = lowest_price -1 #the instruction `cmpwi r3, 4` has a `ble-` comparison after. Therefore we subtract 1 to correclty set the `cmpwi` instruction
            formatted_lowest_price = "{:04X}".format(lowest_price)
            gecko_code_string += replace_characters(can_enter_shop_mp6_gecko_codes[version], 23, formatted_lowest_price)

    print(gecko_code_string)


def replace_characters(string, index, replacement):
    return string[:index] + replacement + string[index + 4:]
    
def load_csv(tab_control, version_var):
    verList = ["JP", "US", "PAL"]
    gameList = ["MP4", "MP5", "MP6"]
    global price_vars
    global weight_vars
    global check_vars
    global checkbuttons
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            data = list(csv_reader)  # Convert csv_reader to list for easy access
            game = data[0]['game']  # First row's game field
            for i in range(3):
                if game == gameList[i]:
                    break

            tab_control.select(frames[i])
            current_tab = tab_control.index("current")
            tab_control.update()
            clear_grid(tab_control)

            text_keys = [row['name'] for row in data]
            text_items = [(row['name'], (row['price'], row['weight'], row['on/off'],)) for row in data]
            #print(text_keys)
            #print(f"Text Items:\n {text_items}")

            create_grid(frames[i], 3, 10, text_keys, text_items, current_tab)
            
            for index, row in enumerate(data):
                price_vars[index].set(row['price'])
                weight_vars[index].set(row['weight'])
                check_vars[index].set(row['on/off'] == 'True')
                on_checkbutton_change(index)  # Update checkbutton widget


def save_csv(tab_control, version_var):
    current_tab = tab_control.index("current")
    #print(f"tab index {current_tab}")

    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])

    if not file_path:
        return

    button_texts = button_texts_list[current_tab]
    version = version_var.get()

    with open(file_path, 'w', newline='') as file:
        fieldnames = ['name', 'price', 'weight', 'on/off', 'game', 'version']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        button_text_keys = list(button_texts.keys())  # Convert keys to a list
        for i in range(len(button_text_keys)):
            weight_value = weight_vars[i].get()
            price_value = price_vars[i].get()
            checked = check_vars[i].get()
            game = f"MP{4 + current_tab}"

            writer.writerow({'name': button_text_keys[i], 'price': price_value, 'weight': weight_value, 'on/off': checked, 'game': game, 'version': version})


def run_gui():
    window = tk.Tk()
    window.title("Mario Party 4/5/6 Item Pool Generator")
    window.iconbitmap("ico/icon.ico")
    window.geometry("600x650")  # Width x Height in pixels

    # Create version_var for save/load csv
    version_var = tk.IntVar(value=1)  # Set default value to 1 (US)

    # # Create version radio buttons
    create_version_buttons(window, version_var)

    # Create the notebook widget
    tab_control = ttk.Notebook(window)

    # Create file menu
    create_file_menu(window, tab_control, version_var)

    # Create tabs for mp4/mp5/mp6
    for _ in range(3):
        frame = ttk.Frame(tab_control)
        frames.append(frame)
        tab_control.add(frame, text=f"MP{4 + _}")

    tab_control.bind("<<NotebookTabChanged>>", lambda event: tab_selected(event, tab_control))
    tab_control.pack(expand=True, fill="both")

    # Create a button frame to hold the buttons
    gen_code_button = tk.Frame(window)
    gen_code_button.pack(side=tk.TOP, fill=tk.X)

    # Create 'Generate Gecko Code' button and add to generate_button
    generate_button = tk.Button(gen_code_button, text="Generate Gecko Code", command=lambda: on_generate_code(tab_control, version_var))
    generate_button.pack(side=tk.LEFT)

    window.mainloop()

if __name__ == "__main__":
    run_gui()