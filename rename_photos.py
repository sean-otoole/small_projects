# execute this script will allow the user to select a folder
# photos and movies, within the folder are then ordered by time when sorting with name

# missing functionality
# check for duplicates and remove
# code added but not yet working

import os
from datetime import datetime
import exifread
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import tkinter as tk
from tkinter import filedialog

def get_the_file_name(current_path):
    new_filename = None  # Initialize new_filename

    # Case-insensitive check for .mov files
    if current_path.lower().endswith('.mov'):
        try:
            parser = createParser(current_path)
            metadata = extractMetadata(parser)
            date_str = (str(metadata).split("Creation date: ")[1])
            creation_date = date_str.split('\n')[0]
            formatted_date = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
            file_extension = os.path.splitext(current_path)[-1]
            new_filename = f"{formatted_date}{file_extension}"
            new_filename = new_filename.replace(" ", "_")
        except Exception as e:
            print(f"Error extracting metadata from '{os.path.basename(current_path)}': {e}")
    
    # Case for image files
    else:
        try:
            with open(current_path, "rb") as file_handle:
                tags = exifread.process_file(file_handle, details=False)
                if 'EXIF DateTimeOriginal' in tags:
                    metadata_str = str(tags['EXIF DateTimeOriginal'])
                    date_obj = datetime.strptime(metadata_str, '%Y:%m:%d %H:%M:%S')
                    filename_date = date_obj.strftime('%Y-%m-%d_%H:%M:%S')
                    file_extension = os.path.splitext(current_path)[-1]
                    new_filename = f"{filename_date}{file_extension}"
                else:
                    print(f"No 'DateTimeOriginal' metadata found for file: {os.path.basename(current_path)}")
        except Exception as e:
            print(f"Error extracting metadata from '{os.path.basename(current_path)}': {e}")

    return new_filename

def rename_files_in_directory(directory_path):
    renamed_files_count = 0  # Initialize the counter for renamed files

    for filename in os.listdir(directory_path):
        current_path = os.path.join(directory_path, filename)
        if os.path.isfile(current_path):  # Check if it's a file
            try:
                new_filename = get_the_file_name(current_path)
                if new_filename:  # Check if a new filename was generated
                    new_path = os.path.join(directory_path, new_filename)
                    
                    # Conflict resolution
                    counter = 1
                    base_new_path, ext = os.path.splitext(new_path)
                    while os.path.exists(new_path):
                        new_path = f"{base_new_path}_{counter}{ext}"
                        counter += 1
                    
                    os.rename(current_path, new_path)
                    print(f"Renamed '{filename}' to '{os.path.basename(new_path)}'")
                    renamed_files_count += 1  # Increment the counter
            except Exception as e:
                print(f"Error processing '{filename}': {e}")

    return renamed_files_count  # Return the count of renamed files

# function for removing duplicate images

def remove_duplicates(directory_path):
    print(directory_path)
    duplicates_removed = 0  # Initialize the counter for removed duplicates
    entries = os.listdir(directory_path)
    all_files = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))]
    print(f"Starting file count: {len(all_files)}")  # sanity check
    for file in all_files:
        if os.path.isfile(os.path.join(directory_path, file)):   #make sure files has not been deleted
            print('we have a file')
            current_index = all_files.index(file);
            if current_index+1 < len(all_files):
                current_file = all_files[current_index]
                adjacent_index = current_index + 1
                adjacent_file = all_files[adjacent_index]
                if open(current_file,"rb").read() == open(adjacent_file,"rb").read():
                    os.remove(adjacent_file)
                    duplicates_removed += 1  # Increment the counter 
                    print('duplicate found, and file removed')
                else:
                    print('no duplicate')
            else:
                print('Finished clearing duplicates')
                break
        else:
            continue # go to the next loop iteration if a file has been deleted
    return duplicates_removed  # Return the count of duplicate files that have been removed

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    directory_path = filedialog.askdirectory()  # Show the dialog and return the selected directory
    return directory_path

# Main execution
if __name__ == "__main__":
    # Prompt the user to select a folder
    directory_path = select_folder()

    if directory_path:  # Proceed only if a folder was selected
        renamed_files_count = rename_files_in_directory(directory_path)
        print(f"Total files renamed: {renamed_files_count}")  # Report the total count of renamed files
        duplicates_removed = remove_duplicates(directory_path)
        print(f"Total duplicates removed: {duplicates_removed}")  # Report the total count of renamed files
    else:
        print("No folder selected, exiting.")

