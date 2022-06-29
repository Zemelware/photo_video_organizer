"""
This program will automatically organize a library of photos and videos into year and month folders using metadata.
"""

import os

import exifread
import exiftool


def get_img_date(img_dir):
    with open(img_dir, 'rb') as image:
        exif_tags = exifread.process_file(image)
        date_time_original = exif_tags['EXIF DateTimeOriginal']
        return date_time_original


def get_video_date(vid_dir):
    with exiftool.ExifTool() as et:
        creation_date = et.get_tag('CreationDate', vid_dir)
        return creation_date


directory = r'./iPhone Photos'
for i, filename in enumerate(os.listdir(directory)):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Image files
        date = get_img_date(os.path.join(directory, filename))
        print(date)
    elif filename.endswith('.mov') or filename.endswith('.mp4'):
        # Video files
        date = get_video_date(os.path.join(directory, filename))
        print(date)
    else:
        print(f"{filename} has an invalid file type.")

# os.makedirs("./Photos/2022/2022-04", exist_ok=True)
# TODO: add loading bar to display progress
