# src/ota_installer/structures/image_file.py
from collections import namedtuple

ImageFile = namedtuple("ImageFile", ["file_path", "directory_path"])

ImageFileData = namedtuple("ImageFileData", ["device", "version"])
