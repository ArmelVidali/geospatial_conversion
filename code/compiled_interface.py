import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import geopandas as gpd
from geo_convert import import_data
import base64


code = base64.b64encode(b"""

# Store the files read by Geopandas along with their fields for later extraction
uploaded_files_fields = {}
# Files read by geopandas
read_files = []


def browse_file():
    # Files accepted by Geopandas
    file_types = [
        ("ESRI Shapefile", "*.shp"),
        ("GeoJSON", "*.geojson"),
        ("GeoPackage", "*.gpkg"),
        ("KML/KMZ", "*.kml;*.kmz"),
        ("MapInfo TAB", "*.tab"),
        ("PostGIS", "postgresql://user:password@localhost:5432/dbname, sql='SELECT * FROM table'"),
        ("Well-Known Text", "*.wkt"),
        ("Spatial Data File", "*.sdf"),
    ]

    file_path = filedialog.askopenfilenames(filetypes=file_types)
    # get EPSG if stated by user
    epsg = int_entry.get()
    if epsg:
        pass
    else:
        epsg = False
    selected_format = option_var.get()

    for path in file_path:
        file = gpd.read_file(path)
        # store each collumns in a global object
        uploaded_files_fields[os.path.basename(path)] = file.columns.tolist()
        # store the geo dataframe
        read_files.append(file)
    show_upload_popup(file_path, selected_format, epsg)

# Display popup with extraction details


def show_upload_popup(loaded_layers_name, selected_format, epsg):
    popup = tk.Toplevel(root)
    popup.title("Couche chargees")
    popup.geometry("1080x900")
    epsg_display = "No EPSG selected"

    # Epsg variable for display purpose
    if epsg == True:
        epsg_display = epsg

    layer_count = tk.Label(popup,
                           text=f"{len(loaded_layers_name)} layer loaded \
                           \n Selected EPSG : {epsg_display}. \
                           \n Selected output format : {selected_format} \
                           ", font=("Arial", 10, "bold"), fg="black")
    layer_count.pack(pady=5)
    layer_count.pack(side="top", anchor="center")

    # List to store the Tkinter IntVar objects associated with each checkbox
    geometry_extraction_checkbox_vars = []
    field_extraction_comboboxes = []

    progress_bar = ttk.Progressbar(popup, mode='indeterminate', length=50)

    # Start taks and set loader
    def start_task():
        global read_files

        # Start the task and remove the start button.
        progress_bar.pack(pady=10, anchor="center")
        progress_bar.start()
        start_button.destroy()
        layer_count.config(text="Work in progress ...")
        # Successfull conversion count
        sucess_count = 0
        # Failed conversion count
        fails = 0
        final_output_path = ""

        for index, gdf in enumerate(read_files):

            field_value = field_extraction_comboboxes[index].get()
            is_checkbox_checked = geometry_extraction_checkbox_vars[index].get(
            )
            # if user selected a value for field extraction
            if field_value != "Choose a field":
                print("------------ Chosen extraction value ------------- ")

                sucess = import_data(
                    gdf, loaded_layers_name[index], selected_format, epsg, True, field_value, bool(is_checkbox_checked))
            else:
                # Convert data without field extraction
                sucess = import_data(
                    gdf, loaded_layers_name[index], selected_format, epsg, extract_invalid_geometry=bool(is_checkbox_checked))
            # Count the number of succesfull conversions
            sucess_count += sucess[0]
            if sucess[0] == 0:
                fails += 1
            final_output_path = sucess[1]

        end_task(sucess_count, final_output_path, fails)
        read_files = []

    # Destroy loadbar and display success message
    def end_task(sucess_count, final_output_path, fails):
        progress_bar.destroy()
        layer_count.config(
            text=f"Conversion finished : {sucess_count} files converted {fails} failed conversions \n Output conversion path : {final_output_path}", fg="green")

    start_button = tk.Button(popup, text="Start Task", command=start_task)
    start_button.pack(pady=10, anchor="center")

    for file in loaded_layers_name:
        # Frame to hold both label and checkboxes
        frame = tk.Frame(popup)
        frame.pack()

        extracted_file_name = os.path.basename(file)

        message_label = tk.Label(frame, text=extracted_file_name, font=(
            "Arial", 12, "bold"), fg="green")
        message_label.pack(side=tk.LEFT, pady=5)

        # Another frame to hold checkboxes horizontally
        checkbox_frame = tk.Frame(frame)
        checkbox_frame.pack(side=tk.RIGHT)

        # Select the field to work with
        combobox = ttk.Combobox(
            checkbox_frame, values=uploaded_files_fields[extracted_file_name])
        combobox.pack(side=tk.LEFT, padx=10)
        field_extraction_comboboxes.append(combobox)

        # Set a default value
        combobox.set("Choose a field")

        # set checkbox for invalid geometry extraction
        geom_var = tk.IntVar()
        geometry_extraction_checkbox_vars.append(geom_var)
        geometry_checkbox = tk.Checkbutton(
            checkbox_frame, text="Extract invalid geometry into a separate folder", variable=geom_var)
        geometry_checkbox.pack(side=tk.LEFT, padx=5)


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
output_type_choice = tk.Label(
    root, text="Choose your output format", font=custom_font, fg="blue")
output_type_choice.pack()

supported_format = tk.Label(
    root, text="Supported format input : .shp, .geojson, .gpkg, .kml/.kmz, .mif/.tab, .dfx, .csv , .json, .gpx, .sqlite/.db", font=("Arial", 10), fg="gray")
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
    tk.Radiobutton(radio_frame, text=option, variable=option_var,
                   value=option).pack(side=tk.LEFT)

# Title: Optional: Choose the output projection for conversion
output_type_choice = tk.Label(
    root, text="Optional: Choose the output projection for conversion (type in the EPSG code, ex: 3857 for Pseudo-Mercator)", fg="gray")
output_type_choice.pack()

# Optional input field
int_entry = tk.Entry(root, validate="key", validatecommand=(
    validate_int_input, '%d', '%P'), width=5)
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
