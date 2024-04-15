from tkinter import Tk, Canvas, Text, Button, PhotoImage, messagebox, filedialog, Menu
import os
import shutil
from pathlib import Path
import openpyxl
from openpyxl.styles import PatternFill

# Define the path to the assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets/frame0")  # Adjust this to your actual assets path

def relative_to_assets(path: str) -> Path:
    """Utility function to get the absolute path to the assets directory."""
    return ASSETS_PATH / Path(path)


# Functions to open directory selection dialogs and insert the chosen path into entry fields
def select_search_folder():
    folder_selected = filedialog.askdirectory()
    entry_1.delete('1.0', 'end')
    entry_1.insert('1.0', folder_selected)


def select_destination_folder():
    folder_selected = filedialog.askdirectory()
    entry_2.delete('1.0', 'end')
    entry_2.insert('1.0', folder_selected)


def find_and_copy_files():
    search_folder = entry_1.get('1.0', 'end').strip()
    destination_folder = entry_2.get('1.0', 'end').strip()
    file_basenames = entry_3.get('1.0', 'end').strip().split('\n')
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    found_files = []
    copy_results = []
    for root, dirs, files in os.walk(search_folder):
        for file in files:
            file_basename, file_extension = os.path.splitext(file)
            if file_basename in file_basenames:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)
                try:
                    shutil.copy2(source_path, destination_path)
                    found_files.append((source_path, destination_path, True))
                except Exception as e:
                    found_files.append((source_path, destination_path, False))
    
    if not found_files:
        messagebox.showinfo("Result", "No files found from the list.")
        return
    
    successful_copies = [f for f in found_files if f[2]]
    failed_copies = [f for f in found_files if not f[2]]
    
    # Update message to include verification result
    if len(successful_copies) == len(found_files):
        messagebox.showinfo("Result", f"Successfully copied {len(successful_copies)} files.")
    else:
        messagebox.showinfo("Result", f"Copied {len(successful_copies)}/{len(found_files)} files. Some files may not have been copied successfully.")
    
    return successful_copies, failed_copies

def export_to_excel(successful_copies, failed_copies):
    # Create a workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    
    # Define fills
    green_fill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')
    red_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
    
    # Write headers
    headers = ['File Path', 'Status']
    ws.append(headers)
    
    # Write data to Excel
    for file in successful_copies:
        ws.append([file[1], 'Success'])
        ws.cell(row=ws.max_row, column=2).fill = green_fill
    
    for file in failed_copies:
        ws.append([file[1], 'Failed'])
        ws.cell(row=ws.max_row, column=2).fill = red_fill
    
    # Save the workbook
    excel_path = os.path.join(OUTPUT_PATH, "copy_results.xlsx")
    wb.save(excel_path)
    messagebox.showinfo("Export Complete", f"Results have been exported to {excel_path}")

def show_about():
    messagebox.showinfo("About", "Extracty\nFor bulk image operations.\nVersion 1.0")

def verify_files_in_destination():
    destination_folder = entry_2.get('1.0', 'end').strip()
    file_basenames = entry_3.get('1.0', 'end').strip().split('\n')
    
    if not os.path.exists(destination_folder):
        messagebox.showinfo("Verification Result", "Destination folder does not exist.")
        return
    
    missing_files = []
    for file_basename in file_basenames:
        files_in_destination = [f for f in os.listdir(destination_folder) if os.path.splitext(f)[0] == file_basename]
        if not files_in_destination:
            missing_files.append(file_basename)
    
    if not missing_files:
        messagebox.showinfo("Verification Result", "All listed files are present in the destination folder.")
    else:
        missing_files_str = ", ".join(missing_files)
        messagebox.showinfo("Verification Result", f"The following files are missing: {missing_files_str}")


window = Tk()
window.geometry("1050x586")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=586, width=1050, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 586,
    width = 1050,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    564.0,
    586.0,
    fill="#1E1E1E",
    outline="")

canvas.create_text(
    38.0,
    27.0,
    anchor="nw",
    text="Extracty\n",
    fill="#EB1616",
    font=("Inter Black", 40 * -1)
)

canvas.create_text(
    38.0,
    77.0,
    anchor="nw",
    text="Bulk Extraction Tool. \nimages in bulk.\n \nThis version is v2.3-CAUST-main.",
    fill="#C9C9C9",
    font=("Inter", 15 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    257.0,
    182.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#3A3A3A",
    fg="#FFFFFF",
    highlightthickness=0,
    font=("Inter Black", 12 * -1)
)
entry_1.place(
    x=32.0,
    y=168.0,
    width=450.0,
    height=26.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=32.0,
    y=202.0,
    width=122.0,
    height=28.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    257.0,
    287.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#3A3A3A",
    fg="#FFFFFF",
    highlightthickness=0,
    font=("Inter Black", 12 * -1)
)
entry_2.place(
    x=32.0,
    y=273.0,
    width=450.0,
    height=26.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=32.0,
    y=307.0,
    width=122.0,
    height=28.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=148.0,
    y=484.0,
    width=218.0,
    height=50.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    809.5,
    312.5,
    image=entry_image_3
)
entry_3 = Text(
    bd=0,
    bg="#3A3A3A",
    fg="#FFFFFF",
    highlightthickness=0,
    font=("Inter Black", 12 * -1)
)
entry_3.place(
    x=564.0,
    y=39.0,
    width=491.0,
    height=545.0
)

canvas.create_rectangle(
    564.0,
    0.0,
    1050.0,
    39.0,
    fill="#EB1616",
    outline="")

canvas.create_text(
    580.0,
    12.0,
    anchor="nw",
    text="Enter file names here.",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

menu_bar = Menu(window, bg="#EB1616", fg="#FFFFFF", relief='flat')
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0, bg="#0C0C0C", fg="#FFFFFF")
menu_bar.add_cascade(label="Verify Destination Extraction", menu=file_menu)
file_menu.add_command(label="Verify Files in Destination", command=verify_files_in_destination)

file_menu = Menu(menu_bar, tearoff=0, bg="#0C0C0C", fg="#FFFFFF")
menu_bar.add_cascade(label="Excel Formatting", menu=file_menu)
file_menu.add_command(label="Excel Formatting", command=verify_files_in_destination)


button_1.configure(command=select_search_folder)
button_2.configure(command=select_destination_folder)
button_3.configure(command=find_and_copy_files)


window.resizable(False, False)
window.mainloop()
