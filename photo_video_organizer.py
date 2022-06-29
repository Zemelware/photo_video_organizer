"""
This program will automatically organize a library of photos and videos into year and month folders using metadata.
"""

import datetime
import os

import exifread
import exiftool


def get_img_date(img_dir):
    with open(img_dir, 'rb') as image:
        exif_tags = exifread.process_file(image)
        date_time_original = exif_tags['EXIF DateTimeOriginal']
        return str(date_time_original)


def get_video_date(vid_dir):
    with exiftool.ExifTool() as et:
        creation_date = et.get_tag('CreationDate', vid_dir)
        return creation_date


directory = r'./photos'
for filename in os.listdir(directory):
    date_str = ''
    invalid_file = False
    filepath = os.path.join(directory, filename)

    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Image files
        date_str = get_img_date(filepath)
    elif filename.endswith('.mov') or filename.endswith('.mp4'):
        # Video files
        date_str = get_video_date(filepath)
    elif os.path.isfile(filepath) and filename != '.DS_Store':
        # Only give an error if the current item is not a folder & not a .DS_Store file
        print(f"The file {filename} has an invalid file type.")
        invalid_file = True
    else:
        invalid_file = True

    if not invalid_file:
        # Remove the part of the date that shows the offset from UTC time (e.g., '-04:00')
        date_str = date_str.split('-', 1)[0]
        # Convert the date string into a date object
        date = datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')

        # The datetime library provides an easy way to get specific parts of a datetime object (in this case the year and month)
        year = date.strftime('%Y')
        month = date.strftime('%m')

        # Variable for the directory format we are going to use
        # Example of this format: 2022/2022-03
        new_dir = f"./photos/{year}/{year}-{month}"
        new_filepath = os.path.join(new_dir, filename)

        # After looking at each file, create new directories with the photo/video's year and month
        # E.g., if a photo was taken in December of 2018, the folders 2018/2018-12 will be created
        # If the folder already exists (meaning another photo/video was taken in the same month/year) then no error will be thrown
        os.makedirs(new_dir, exist_ok=True)

        # Move the file into its appropriate directory based on the date the photo/video was taken
        os.replace(filepath, new_filepath)

        # Rename the file to the day/time it was taken so all photos/videos are organized by date taken
        new_name = os.path.join(new_dir, date.strftime('%Y-%m-%d %H-%M'))
        # In the 2nd argument of the function below, the extension is added to the name of the file
        os.rename(new_filepath, new_name + os.path.splitext(filename)[1])

# TODO: add loading bar to display progress
