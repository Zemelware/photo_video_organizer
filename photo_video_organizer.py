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
for i, filename in enumerate(os.listdir(directory)):
    date_str = ''
    invalid_file = False

    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Image files
        date_str = get_img_date(os.path.join(directory, filename))
    elif filename.endswith('.mov') or filename.endswith('.mp4'):
        # Video files
        date_str = get_video_date(os.path.join(directory, filename))
    else:
        print(f"{filename} has an invalid file type.")
        invalid_file = True

    if not invalid_file:
        date_str = date_str.split('-', 1)[0]
        date = datetime.datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        print(date)

# os.makedirs("./Photos/2022/2022-04", exist_ok=True)
# TODO: add loading bar to display progress
