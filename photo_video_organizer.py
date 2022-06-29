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
    else:
        print(f"{filename} has an invalid file type.")
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

        # After looking at each file, create new directories with the photo/video's year and month
        # E.g., if a photo was taken in December of 2018, the folders 2018/2018-12 will be created
        # If the folder already exists (meaning another photo/video was taken in the same month/year) then no error will be thrown
        os.makedirs(new_dir, exist_ok=True)
        # Move the file into its appropriate directory based on the date the photo/video was taken
        os.replace(filepath, os.path.join(new_dir, filename))

# TODO: add loading bar to display progress
