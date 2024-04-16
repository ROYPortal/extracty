from tkinter import Tk, Canvas, Text, Button, PhotoImage, messagebox, filedialog, Menu
import os
import shutil
from pathlib import Path
import openpyxl
from openpyxl.styles import PatternFill
import subprocess
import requests
import semver


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets/frame0")  # Adjust this to your actual assets path


def relative_to_assets(path: str) -> str:
    """Utility function to get the absolute path to the assets directory."""
    return os.path.join(ASSETS_PATH, path)

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
    file_basenames = set(entry_3.get('1.0', 'end').strip().split('\n'))
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    successful_copies = 0
    unsuccessful_copies = len(file_basenames)  # Start with all as unsuccessful

    for root, dirs, files in os.walk(search_folder):
        for file in files:
            file_basename, file_extension = os.path.splitext(file)
            if file_basename in file_basenames:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_folder, file)
                # Before copying, check if the destination file already exists
                if not os.path.exists(destination_path):
                    try:
                        shutil.copy2(source_path, destination_path)
                        successful_copies += 1
                        unsuccessful_copies -= 1  # One less unsuccessful copy
                    except Exception as e:
                        pass  # Unsuccessful copy remains counted

    # Display a simple message box with the results
    messagebox.showinfo("Copy Results", f"{successful_copies} Successful | {unsuccessful_copies} Unsuccessful")









def verify_files_in_destination():
    destination_folder = entry_2.get('1.0', 'end').strip()
    file_basenames = entry_3.get('1.0', 'end').strip().split('\n')
    
    if not os.path.exists(destination_folder):
        messagebox.showinfo("Verification Result", "Destination folder does not exist.")
        return
    
    # Create a new workbook and select the active worksheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = 'Item'
    sheet['B1'] = 'Status'
    
    # Collect all files in the destination folder for faster checking
    existing_files = set(os.listdir(destination_folder))
    existing_basenames = {os.path.splitext(file)[0] for file in existing_files}  # Store without extensions

    # Check each file and write its status to the sheet
    for row_index, file_basename in enumerate(file_basenames, start=2):
        status = 'FOUND' if file_basename in existing_basenames else 'FAILED'
        sheet.cell(row=row_index, column=1, value=file_basename)
        sheet.cell(row=row_index, column=2, value=status)
    
    # Save the workbook and ask user for the save location
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
        title="Save the verification result as..."
    )
    
    if file_path:  # Check if the user didn't cancel the save dialog
        workbook.save(file_path)
        messagebox.showinfo("Verification Complete", f"The verification result has been saved to:\n{file_path}")







def get_current_version():
    try:
        with open('version.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "0.0.0"  # Default to 0.0.0 if version.txt does not exist

def get_latest_version():
    try:
        response = requests.get('https://raw.githubusercontent.com/ROYPortal/extracty/main/version.txt')
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text.strip()
    except requests.RequestException as e:
        print("Failed to fetch the latest version:", e)
        return None

def download_update():
    try:
        updated_script_url = 'https://raw.githubusercontent.com/ROYPortal/extracty/main/app.py'
        response = requests.get(updated_script_url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print("Failed to download the update:", e)
        return None

def apply_update(update_content):
    try:
        with open('app.py', 'w') as file:
            file.write(update_content)
        return True
    except IOError as e:
        print("Failed to apply update:", e)
        return False

def main():
    local_version = get_current_version()
    remote_version = get_latest_version()

    if remote_version and semver.compare(remote_version, local_version) > 0:
        print(f"An update is available: {local_version} -> {remote_version}")
        update_content = download_update()
        if update_content:
            if input("Would you like to apply the update now? (y/n): ").lower() == 'y':
                if apply_update(update_content):
                    print("Update applied successfully. Please restart the application.")
                else:
                    print("Update failed to apply.")
            else:
                print("Update cancelled by the user.")
    elif remote_version:
        print("You are up to date!")
    else:
        print("Could not check for updates due to an earlier error.")

if __name__ == '__main__':
    main()




    




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
    text="Bulk Extraction Tool. \nimages in bulk. Made by Liam Caust @ Galvins Plumbing Supplies\n \nThis version is v2.8-CAUST-branch02.\n",
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



button_1.configure(command=select_search_folder)
button_2.configure(command=select_destination_folder)
button_3.configure(command=find_and_copy_files)


window.resizable(False, False)
window.mainloop()
