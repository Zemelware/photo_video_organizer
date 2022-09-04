"""
Author: Ethan Zemelman
Date: 2022/06/29
Purpose: This program will automatically organize a library of photos and videos into year and month folders using metadata attached to the files.
"""

import datetime
import os
import sys

import exifread
import exiftool
from tqdm import tqdm


def get_img_date(img_path):
    with open(img_path, 'rb') as image:
        exif_tags = exifread.process_file(image)
        date_time_original = exif_tags['EXIF DateTimeOriginal']
        return str(date_time_original)


def get_video_date(vid_path):
    with exiftool.ExifTool() as et:
        creation_date = et.get_tag('CreationDate', vid_path)
        if creation_date is None:
            # Some videos don't have the CreationDate tag, so we use the DateTimeOriginal tag instead
            creation_date = et.get_tag('DateTimeOriginal', vid_path)
        if creation_date is None:
            # If creation_date is None, it means the tag couldn't be found
            raise Exception(
                f'No CreationDate or DateTimeOriginal metadata tag associated with {vid_path}')
        return creation_date


if len(sys.argv) < 2:
    print(
        "\033[91mYou must pass in the path of the directory that contains your photos and videos.\033[0m")
    exit()

print("Organizing your library...")

directory = sys.argv[1]

for filename in tqdm(os.listdir(directory)):
    date_str = ''
    invalid_file = False
    filepath = os.path.join(directory, filename)

    if not filename.startswith('.'):  # ignore hidden files
        if filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.jpeg') or filename.endswith('.JPEG') or filename.endswith('.png') or filename.endswith('.PNG') or filename.endswith('.heic') or filename.endswith('.HEIC'):
            # Image files
            try:
                date_str = get_img_date(filepath)
            except:
                print(f"\033[91mNo date information for '{filename}'\033[0m")
                invalid_file = True
        elif filename.endswith('.mov') or filename.endswith('.MOV') or filename.endswith('.mp4') or filename.endswith('.MP4'):
            # Video files
            try:
                date_str = get_video_date(filepath)
            except:
                print(f"\033[91mNo date information for '{filename}'\033[0m")
                invalid_file = True
        elif os.path.isfile(filepath) and filename != '.DS_Store':
            # Only give an error if the current item is not a folder & not a .DS_Store file
            print(
                f"\033[91mThe file '{filename}' has an invalid file type.\033[0m")
            invalid_file = True
        else:
            invalid_file = True
    else:
        invalid_file = True

    if not invalid_file:
        # Remove the part of the date that shows the offset from UTC time (e.g., '-04:00')
        date_str = date_str.split('-', 1)[0]
        date_str = date_str.split('+', 1)[0]
        # Convert the date string into a date object
        date = datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')

        # The datetime library provides an easy way to get specific parts of a datetime object (in this case the year and month)
        year = date.strftime('%Y')
        month = date.strftime('%m')

        # Variable for the directory format we are going to use
        # Example of this format: 2022/2022-03
        new_dir = os.path.join(directory, f"{year}/{year}-{month}")
        new_filepath = os.path.join(new_dir, filename)

        # After looking at each file, create new directories with the photo/video's year and month
        # E.g., if a photo was taken in December of 2018, the folders 2018/2018-12 will be created
        # If the folder already exists (meaning another photo/video was taken in the same month/year) then no error will be thrown
        os.makedirs(new_dir, exist_ok=True)

        # Move the file into its appropriate directory based on the date the photo/video was taken
        os.replace(filepath, new_filepath)

        # Rename the file to the day/time it was taken so all photos/videos are organized by date taken
        new_name = os.path.join(new_dir, date.strftime('%Y-%m-%d %H-%M'))
        file_ext = os.path.splitext(filename)[1]
        # Handle duplicate file names
        uniq = 1
        while os.path.exists(new_name + file_ext):
            # Add a number at the end of the file name to make it unique
            new_name = os.path.join(new_dir, date.strftime(
                '%Y-%m-%d %H-%M')) + f" ({uniq})"
            uniq += 1
        os.rename(new_filepath, new_name + file_ext)
