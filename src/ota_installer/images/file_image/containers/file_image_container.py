# src/ota_installer/images/file_image/containers/file_image_container.py
from collections import namedtuple

"""Represents file and directory paths for a file image."""
FileImagePaths = namedtuple("FileImagePaths", ["file_path", "directory_path"])

"""Contains information about the file image data."""
FileImageData = namedtuple("FileImageData", ["device", "version"])

"""Defines the structure of a file image with title and extension."""
FileImageStruct = namedtuple("FileImageStruct", ["title", "extension"])
# Signed off by Brian Sanford on 20260116
