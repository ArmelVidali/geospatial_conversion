import tkinter as tk
from tkinter import filedialog
from geo_convert import import_data
import base64

code = base64.b64encode(b"""

def browse_file():
    file_path = filedialog.askopenfilenames()
    epsg = int_entry.get()
    if epsg:
        pass
    else:
        epsg = False
    selected_format = option_var.get()
    print(selected_format)
    count = 0 
    
    for element in file_path:
        success = import_data(element, selected_format, epsg)
        if success[0]:
            count +=1

    if count : 
        show_confirmation_popup(True, success[1], count)
    else :
        show_confirmation_popup(False)

def show_confirmation_popup(success , path = "", count = 0):
    if success : 
        popup = tk.Toplevel(root)
        popup.title("Success")
        popup.geometry("380x150")

        message_label = tk.Label(popup, text="Files successfully converted", font=("Arial", 12, "bold"), fg = "green")
        message_label.pack(pady=20)
        path_label = tk.Label(popup, text= str(count) + " file.s was converted to the " + path + " folder", font=("Arial", 10))
        path_label.pack(pady=20)

    else : 
        popup = tk.Toplevel(root)
        popup.title("Error")
        popup.geometry("350x150")

        message_label = tk.Label(popup, text="An error occured", font=("Arial", 12, "bold"), fg = "red")
        message_label.pack(pady=20)

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
root.title("Geographic File Converter")
root.geometry("600x300")

font_family = "Arial"
font_size = 16
font_weight = "bold"
font_color = "red"

custom_font = (font_family, font_size, font_weight)

# Title: Choose your output format
output_type_choice = tk.Label(root, text="Choose your output format", font=custom_font, fg="blue")
output_type_choice.pack()

supported_format = tk.Label(root, text="Supported format input : .shp, .geojson, .gpkg, .kml/.kmz, .mif/.tab, .dfx, .csv , .json, .gpx, .sqlite/.db", font=("Arial", 10), fg="gray")
supported_format.pack()

options = ["geojson", "gpkg", "shp", "csv", "dfx"]

# Variable to store the selected option
option_var = tk.StringVar()
option_var.set(options[0])

# Frame to hold the radio buttons and optional input field
radio_frame = tk.Frame(root)
radio_frame.pack()

# Create the radio buttons in a horizontal row inside the frame
for option in options:
    tk.Radiobutton(radio_frame, text=option, variable=option_var, value=option).pack(side=tk.LEFT)

# Title: Optional: Choose the output projection for conversion
output_type_choice = tk.Label(root, text="Optional: Choose the output projection for conversion (type in the EPSG code, ex: 3857 for Pseudo-Mercator)", fg="gray")
output_type_choice.pack()

# Optional input field
int_entry = tk.Entry(root, validate="key", validatecommand=(validate_int_input, '%d', '%P'), width=5)
int_entry.pack()

int_entry.bind("<Return>", stop_blinking_cursor)
int_entry.bind("<FocusOut>", stop_blinking_cursor)

# Text
text_label = tk.Label(root, text="Browse for files/folder")
text_label.pack(pady=(20, 0))

# Button to browse file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=10)

root.mainloop()
""")

exec(base64.b64decode(code))