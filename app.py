from tkinter import Tk, Canvas, Text, Button, PhotoImage, messagebox, filedialog, Menu, ttk, Entry, Toplevel, Scrollbar



import os



import shutil



from pathlib import Path



import openpyxl



from openpyxl.styles import PatternFill



import subprocess



import requests



import semver



import logging





OUTPUT_PATH = Path(__file__).parent



ASSETS_PATH = OUTPUT_PATH / Path("./assets/frame0")  # Adjust this to your actual assets path



















########################################################################################################## OPERATIONS CODE 


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

def find_and_copy_files(entry_1: Entry, entry_2: Entry, entry_3: Entry):
    search_folder = entry_1.get('1.0', 'end').strip()
    destination_folder = entry_2.get('1.0', 'end').strip()
    file_basenames = entry_3.get('1.0', 'end').strip().split('\n')

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    copy_success = set()  # Using a set to store successful file names
    copy_failures = set()  # Using a set to store failed file names

    for file_basename in file_basenames:
        found_file = False  # Flag to check if file is found in the search folder

        for root, dirs, files in os.walk(search_folder):
            if found_file:
                break  # If file is found, no need to continue the search

            for file in files:
                current_file_basename, file_extension = os.path.splitext(file)
                
                if current_file_basename == file_basename:
                    source_path = os.path.join(root, file)
                    destination_path = os.path.join(destination_folder, file)
                    found_file = True  # Set the flag as file is found

                    # Check if the file already exists in the destination
                    if os.path.exists(destination_path):
                        copy_failures.add(file_basename)
                    else:
                        try:
                            shutil.copy2(source_path, destination_path)
                            copy_success.add(file_basename)
                        except Exception as e:
                            copy_failures.add(file_basename)
                    break  # No need to search further as file is processed

        if not found_file:
            copy_failures.add(file_basename)  # If file was not found, mark as failure

    # Convert the sets to sorted lists for consistent ordering
    copy_success = sorted(list(copy_success))
    copy_failures = sorted(list(copy_failures))

    # Prepare the results text
    success_string = "\n".join(f"{filename}\tSuccessful" for filename in copy_success)
    failure_string = "\n".join(f"{filename}\tUnsuccessful" for filename in copy_failures)
    results_text = f"Successful Copies:\n{success_string}\n\nFailed Copies:\n{failure_string}"

    # Create a new Toplevel window to display results
    result_window = Toplevel()
    result_window.title("Copy Results")

    # Create a Text widget with a Scrollbar inside the Toplevel window
    text_area = Text(result_window, height=15, width=50)
    text_area.pack(side='left', fill='both', expand=True)

    # Insert the results into the Text widget
    text_area.insert('1.0', results_text)

    # Add a Scrollbar and set it to scroll the Text widget content
    scrollbar = Scrollbar(result_window, command=text_area.yview)
    scrollbar.pack(side='right', fill='y')
    text_area['yscrollcommand'] = scrollbar.set



##########################################################################################################




















########################################################################################################## GIT UPDATE


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_current_version():

    try:

        with open('version.txt', 'r') as file:

            version = file.read().strip()

            if semver.VersionInfo.isvalid(version):

                return version

            else:

                logging.error("Invalid version format in local version file.")

                return "0.0.0"

    except FileNotFoundError:

        logging.warning("Local version file not found. Assuming version 0.0.0.")

        return "0.0.0"



def get_latest_version():

    try:

        response = requests.get('https://raw.githubusercontent.com/ROYPortal/extracty/main/version.txt', timeout=10)

        response.raise_for_status()

        latest_version = response.text.strip()

        if semver.VersionInfo.isvalid(latest_version):

            return latest_version

        else:

            logging.error("Invalid version format in fetched version file.")

            return None

    except requests.RequestException as e:

        logging.error("Failed to fetch the latest version: {e}")

        return None



def download_file(url, path):

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        with open(path, 'w') as file:

            file.write(response.text)

        logging.info(f"{path} downloaded and updated successfully.")

        return True

    except requests.RequestException as e:

        logging.error(f"Failed to download {path}: {e}")

        return False



def apply_update(new_version):

    app_success = download_file('https://raw.githubusercontent.com/ROYPortal/extracty/main/app.py', 'app.py')

    version_success = download_file('https://raw.githubusercontent.com/ROYPortal/extracty/main/version.txt', 'version.txt')



    if app_success and version_success:

        logging.info(f"Update applied successfully to version {new_version}. Please restart the application.")

        return True

    else:

        logging.error("Failed to apply update completely.")

        return False



def check_for_updates():

    local_version = get_current_version()

    remote_version = get_latest_version()

    if remote_version and semver.compare(remote_version, local_version) > 0:

        print(f"An update is available: {local_version} -> {remote_version}")

        user_response = input("Would you like to apply the update now? (yes/no): ")

        if user_response.lower() in ['yes', 'y']:

            apply_update(remote_version)

        else:

            print("Update cancelled by the user.")

    elif remote_version:

        print("You are up to date!")

    else:

        print("Could not check for updates due to an earlier error.")



if __name__ == "__main__":

    check_for_updates()





########################################################################################################## 





































########################################################################################################## GUI CODE



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



    text="Bulk Extraction Tool. \nThis version is v1.0.6-CAUST-branch02.\n",



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



    text="Enter file names here. Case sensitive. Remove extensions on list",



    fill="#FFFFFF",



    font=("Inter", 15 * -1)



)



canvas.create_text(



    140.0,



    450.0,



    anchor="nw",



    text="Dont Let Liam code again! He's shit!",



    fill="#FFFFFF",



    font=("Inter", 15 * -1)



)



canvas.create_text(



    30.0,



    250.0,



    anchor="nw",



    text="Destination Folder",



    fill="#FFFFFF",



    font=("Inter", 15 * -1)



)



canvas.create_text(



    30.0,



    145.0,



    anchor="nw",



    text="Viewing Folder",



    fill="#FFFFFF",



    font=("Inter", 15 * -1)



)





menu_bar = Menu(window, bg="#EB1616", fg="#FFFFFF", relief='flat')



window.config(menu=menu_bar)







button_1.configure(command=select_search_folder)



button_2.configure(command=select_destination_folder)



button_3.configure(command=lambda: find_and_copy_files(entry_1, entry_2, entry_3))












window.resizable(False, False)



window.mainloop()
