from PIL import Image
import piexif
def resize_to_square(image_input, size=1080):
    """
    Resize an image to a square format by cropping the center.

    Parameters:
        image_input (str or PIL.Image): Path to the input image or already loaded PIL image.
        size (int): Desired square size (default is 1080).

    Returns:
        PIL.Image: The resized square image.
        Raises ValueError or TypeError on error.
    """
    if isinstance(image_input, str):
        try:
            img = Image.open(image_input).convert("RGB")
        except FileNotFoundError:
            raise ValueError(f"Image not found at {image_input}")
        except Exception as e:
            raise ValueError(f"Error opening image at {image_input}: {e}")
    elif isinstance(image_input, Image.Image):
        img = image_input.convert("RGB")
    else:
        raise TypeError("image_input must be a string (path) or a PIL.Image object.")

    # Extract EXIF data using piexif
    exif_dict = piexif.load(img.info['exif']) if 'exif' in img.info else {}
    orientation_tag = piexif.ImageIFD.Orientation
    if orientation_tag in exif_dict.get('0th', {}):
        orientation = exif_dict['0th'][orientation_tag]
        if orientation == 3:
            img = img.rotate(180, expand=True)
        elif orientation == 6:
            img = img.rotate(270, expand=True)
        elif orientation == 8:
            img = img.rotate(90, expand=True)

    width, height = img.size

    # Calculate cropping box
    if width != height:
        smaller_side = min(width, height)
        left = (width - smaller_side) / 2
        top = (height - smaller_side) / 2
        right = (width + smaller_side) / 2
        bottom = (height + smaller_side) / 2
        img = img.crop((left, top, right, bottom))

    # Resize to the desired square size
    img = img.resize((size, size), Image.BICUBIC)

    return img



import requests

def get_coordinates_from_name(location_name):
    """
    Use a geocoding API to get the latitude and longitude of a location by name.
    Here, we use OpenStreetMap's Nominatim API.
    """
    print(f"Search coordinates for name: {location_name}")
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
    }
    url = f"https://nominatim.openstreetmap.org/search?q={location_name}&format=json"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            results = response.json()
            if results:
                lat = float(results[0]['lat'])
                lon = float(results[0]['lon'])
                return lat, lon
        else:
            print(f"Error: {response.status_code}, {response.reason}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return None, None


import math
import random


def randomize_coordinates(lat, lon, range_km):
    """
    Randomize coordinates within a given range of kilometers from a given point.

    Parameters:
    lat, lon - Latitude and Longitude of the central point in decimal degrees
    range_km - Range in kilometers within which to randomize coordinates

    Returns:
    A tuple of randomized (latitude, longitude)
    """
    # Earth's radius in kilometers
    R = 6371

    # Convert range from kilometers to radians
    range_rad = range_km / R

    # Generate a random angular distance and bearing
    random_distance = random.uniform(0, range_rad)
    random_bearing = random.uniform(0, 2 * math.pi)

    # Calculate the new latitude
    new_lat = math.asin(
        math.sin(math.radians(lat)) * math.cos(random_distance) +
        math.cos(math.radians(lat)) * math.sin(random_distance) * math.cos(random_bearing)
    )

    # Calculate the new longitude
    new_lon = math.radians(lon) + math.atan2(
        math.sin(random_bearing) * math.sin(random_distance) * math.cos(math.radians(lat)),
        math.cos(random_distance) - math.sin(math.radians(lat)) * math.sin(new_lat)
    )

    # Convert radians back to degrees
    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)

    return new_lat, new_lon


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth.
    Parameters:
    lat1, lon1 - Latitude and Longitude of point 1 in decimal degrees
    lat2, lon2 - Latitude and Longitude of point 2 in decimal degrees
    Returns:
    Distance in kilometers
    """
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def remove_first_and_last_from_str(input_string):
    """
    Removes double quotes (") from the first and last 3 characters of a string.
    If the string length is 6 or less, removes double quotes from all characters.

    Args:
        input_string: The string to modify.

    Returns:
        The modified string, or the original string if the input is empty.
    """
    if not input_string:  # Check for an empty string
        return input_string

    if len(input_string) <= 6:  # If string length is 6 or less
        return input_string.replace('"', '')

    # For strings longer than 6, process the first and last 3 characters
    first_part = input_string[:3].replace('"', '')
    middle_part = input_string[3:-3]
    last_part = input_string[-3:].replace('"', '')

    return first_part + middle_part + last_part