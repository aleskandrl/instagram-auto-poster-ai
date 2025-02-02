import os
from google.cloud import vision
import os
from google.cloud import vision


class BaseImageAnalyzer:
    """Abstract base class for an Image Analyzer."""

    def analyze_image(self, image_path):
        """Analyze an image and return labels."""
        raise NotImplementedError("This method should be overridden in a subclass.")



class GoogleVisionImageAnalyzer(BaseImageAnalyzer):
    """Implementation of ImageAnalyzer using Google Vision API."""

    def __init__(self, credentials_path):
        # Set up Google Vision API credentials
        self.credentials_path = credentials_path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        self.client = vision.ImageAnnotatorClient()

    def analyze_image(self, image_path):
        """Analyze an image using Google Vision API and return labels."""
        with open(image_path, "rb") as image_file:
            content = image_file.read()
            image = vision.Image(content=content)

        response = self.client.label_detection(image=image)

        if response.error.message:
            raise Exception(f"Google Vision API Error: {response.error.message}")

        labels = [label.description for label in response.label_annotations]
        return labels


class EmptyImageAnalyzer(BaseImageAnalyzer):
    """Dummy implementation of an Image Analyzer with no functionality."""

    def analyze_image(self, image_path):
        return []



# Factory function to create the appropriate Image Analyzer
def create_image_analyzer(use_google_vision, credentials_path=None):
    """
    Factory to create either a GoogleVisionImageAnalyzer or EmptyImageAnalyzer.

    Parameters:
    use_google_vision (bool): Whether to use the Google Vision API.
    credentials_path (str): Path to the credentials file for Google Vision API (required if use_google_vision is True).

    Returns:
    BaseImageAnalyzer: An instance of GoogleVisionImageAnalyzer or EmptyImageAnalyzer.
    """
    if use_google_vision:
        print("Google_vision in use")
        if not credentials_path:
            raise ValueError("Credentials path is required when use_google_vision is True.")
        return GoogleVisionImageAnalyzer(credentials_path=credentials_path)
    else:
        print("Google_vision not in use")
        return EmptyImageAnalyzer()




# Example usage
from configuration import GOOGLE_CREDENTIALS_PASS

if __name__ == "__main__":
    use_google_vision = True  # Set to False to disable Google Vision functionality
    analyzer = create_image_analyzer(use_google_vision, GOOGLE_CREDENTIALS_PASS)

    image_path = "D://2.dev//1.src//InstaPoster//images//20241129_013436.jpg"  # Replace with the path to your image

    result = analyzer.analyze_image(image_path)
    print(result)


