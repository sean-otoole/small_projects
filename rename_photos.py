# execute this script in a directory containing photos and movies and all files will be renamed with the date and time of acquisition
# photos and movies are then ordered by time when sorting with name

import os
from datetime import datetime
import exifread
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def get_the_file_name(current_path):
    new_filename = None  # Initialize new_filename

    # Check if the file is a movie
    if current_path.lower().endswith('.mov'):
        parser = createParser(current_path)
        metadata = extractMetadata(parser)
        if metadata and 'creation_date' in metadata:
            date = metadata.get('creation_date')
            formatted_date = date.strftime('%Y-%m-%d_%H-%M-%S')
            new_filename = f"{formatted_date}.mov"
    
    # Check if the file is an image
    else:
        with open(current_path, "rb") as file_handle:
            tags = exifread.process_file(file_handle, details=False)
            if 'EXIF DateTimeOriginal' in tags:
                metadata_str = str(tags['EXIF DateTimeOriginal'])
                date_obj = datetime.strptime(metadata_str, '%Y:%m:%d %H:%M:%S')
                filename_date = date_obj.strftime('%Y-%m-%d_%H-%M-%S')
                file_extension = os.path.splitext(current_path)[-1]
                new_filename = f"{filename_date}{file_extension}"

    return new_filename

def rename_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        current_path = os.path.join(directory_path, filename)
        if os.path.isfile(current_path):  # Check if it's a file
            new_filename = get_the_file_name(current_path)
            if new_filename:  # Check if a new filename was generated
                new_path = os.path.join(directory_path, new_filename)
                os.rename(current_path, new_path)
                print(f"Renamed '{filename}' to '{new_filename}'")

# Specify the directory path here
directory_path = getcwd()
rename_files_in_directory(directory_path)
