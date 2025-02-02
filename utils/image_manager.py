import json
import os

class ImageManager:
    """
    A class to manage image-related operations, including resizing and tracking image metadata.
    """

    def __init__(self, folder_path):
        """
        Initialize the ImageManager with a log file.

        Parameters:
            folder_path (str): Path to the log file.
        """
        self.log_file = folder_path + "//log.json"

        # Initialize the log file if it doesn't exist
        try:
            with open(self.log_file, 'r') as file:
                json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.log_file, 'w') as file:
                json.dump([], file)

    def add_image_to_log(self, image_path, additional_info=None):
        """
        Add an image and its additional information to the log file.

        Parameters:
            image_path (str): Path to the image file.
            additional_info (dict, optional): Additional information about the image.
        """
        image_name = os.path.basename(image_path)

        with open(self.log_file, 'r') as file:
            data = json.load(file)

        # Check if the image is already in the log
        if self.is_image_in_log(image_name):
            print(f"Image '{image_name}' is already in the log.")
            return

        # Add the new image entry
        entry = {"image_name": image_name}
        if additional_info:
            entry.update(additional_info)
        data.append(entry)

        # Save the updated log
        with open(self.log_file, 'w') as file:
            json.dump(data, file, indent=4)

    def is_image_in_log(self, image_name):
        """
        Check if an image is already in the log file.

        Parameters:
            image_name (str): Name of the image file to check.

        Returns:
            bool: True if the image is in the log, False otherwise.
        """
        with open(self.log_file, 'r') as file:
            data = json.load(file)

        return any(entry.get("image_name") == image_name for entry in data)


# Example usage
#manager = ImageManager('images/image_log.json')
#manager.add_image_to_log('D://2.dev//1.src//InstaPoster//images//20231006_115929.jpg', {"size": "1080x1080", "format": "JPEG"})
#print(manager.is_image_in_log('20231006_115930.jpg'))  # This should now return True
