import tkinter as tk
from tkinter import filedialog
from geo_convert import import_data

def browse_file():
    file_path = filedialog.askopenfilenames()
    epsg = int_entry.get()
    if epsg :
        pass
    else :
        epsg = False
    selected_format = option_var.get()
    
    for element in file_path:
        import_data(element, selected_format, epsg)

def select_output_type():
    # Implement the logic to select the type of output file here
    print("Output type selected")

def validate_int_input(action, value_if_allowed):
    if action == '1':  # Insertion or deletion of text
        # Check if the new value is an integer or an empty string (allowing deletion)
        return value_if_allowed.isdigit() or value_if_allowed == ""
    return True  # Accept any other actions    

def stop_blinking_cursor(event):
    int_entry.configure(validate="none")
    root.focus()  # Set focus to the root window to remove focus from the input field

root = tk.Tk()
root.title("Geogrphic file converter")
root.geometry("600x600")

font_family = "Arial"
font_size = 16
font_weight = "bold"
font_color = "red"

custom_font = (font_family, font_size, font_weight)


# Button to select the type of output file
output_type_choice = tk.Label(root, text="Choose your ouput format", font=custom_font, fg="blue")
output_type_choice.pack()

options = ["GeoJson", "Geopackage", "Shapefile","csv"]

option_var = tk.StringVar(root)
option_var.set(options[0])  # Set the default selected option

option_menu = tk.OptionMenu(root, option_var, *options)
option_menu.pack()

output_type_choice = tk.Label(root, text="Optionnal : Choose the output projection for conversion (type in the EPSG code, ex : 3857 for Pseudo-Mercator)", fg="gray")
output_type_choice.pack()
int_entry = tk.Entry(root, validate="key", validatecommand=(validate_int_input, '%d', '%P'), width=5)
int_entry.pack()



int_entry.bind("<Return>", stop_blinking_cursor)
int_entry.bind("<FocusOut>", stop_blinking_cursor)

options = ["GeoJson", "Geopackage"]

option_var = tk.StringVar(root)
option_var.set(options[0])  # Set the default selected option

option_menu = tk.OptionMenu(root, option_var, *options)
option_menu.pack()



# Text
text_label = tk.Label(root, text="Browse for files/folder")
text_label.pack(pady=(20,0))

# Button to browse file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)



root.mainloop()
