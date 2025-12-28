# src/ota_installer/images/file_image/containers/file_image_container.py
from collections import namedtuple

FileImagePaths = namedtuple("FileImagePaths", ["file_path", "directory_path"])

FileImageData = namedtuple("FileImageData", ["device", "version"])

FileImageStruct = namedtuple("FileImageStruct", ["title", "extension"])
