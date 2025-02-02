from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image
from utils.utils import resize_to_square
import os
import io

def extract_location_from_metadata(image):
    """
    Extracts GPS metadata from the image and converts it to a format compatible with instagrapi.
    Returns None if no GPS metadata is available.
    """
    try:
        exif_data = image._getexif()
        if not exif_data:
            return None

        gps_info = {}
        for tag, value in exif_data.items():
            decoded_tag = TAGS.get(tag, tag)
            if decoded_tag == "GPSInfo":
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_info[sub_decoded] = value[t]
                break

        if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
            lat = convert_to_degrees(gps_info["GPSLatitude"])
            if gps_info.get("GPSLatitudeRef") == "S":
                lat = -lat

            lon = convert_to_degrees(gps_info["GPSLongitude"])
            if gps_info.get("GPSLongitudeRef") == "W":
                lon = -lon

            # Return as a dictionary compatible with instagrapi
            return {"lat": lat, "lng": lon}

    except Exception as e:
        print(f"Error extracting metadata: {e}")

    return None

def convert_to_degrees(value):
    """
    Converts GPS coordinates stored as degrees, minutes, and seconds
    to decimal degrees.
    """
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

class Post:
    """
    Represents a single Instagram post.
    """

    def __init__(self, image_data, location=None, description=""):
        if isinstance(image_data, str):
            self._image = Image.open(image_data)
            self._image_path = image_data
        elif isinstance(image_data, Image.Image):
            self._image = image_data
            self._image_path = None
        elif isinstance(image_data, io.BytesIO):
            self._image = Image.open(image_data)
            self._image_path = None
        else:
            raise ValueError("image_data must be a path, image object, or BytesIO object")

        self._description = description
        self._raw_location = location or extract_location_from_metadata(self._image)
        self._location = None  # Placeholder for an instagrapi-compatible location object


    def resize_to_square(self):
         self._image = resize_to_square(self._image, 1080)

    @property
    def image(self):
        return self._image

    @property
    def image_path(self):
        return self._image_path

    @property
    def image_name(self):
        if self._image_path:
            return os.path.basename(self._image_path)
        return "Untitled"

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
       self._location=location

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description


    def as_dict(self):
        return {
            "image_path": self.image_path,
            "description": self.description,
            "location": self.location,
        }
