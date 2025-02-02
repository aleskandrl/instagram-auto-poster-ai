from collections import namedtuple
from instagrapi import Client
from defines.post import *
from utils.image_manager import *
from utils.utils import *
from openai_api.openai_chatgpt import *
from google_api.google_image_analyzer import *

from configuration import *
from utils.scheduler import *

class Poster:
    """
    Handles Instagram login and posting.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = Client()
        self.posts = []
        self.google_image_analyzer = None
        self.openai_chat = None

        self.google_image_analyzer = create_image_analyzer(USE_AI, GOOGLE_CREDENTIALS_PASS)
        print("Image analyzer loaded!")

        self.openai_chat = create_chat_client(USE_AI, OPENAI_API_KEY)
        print("Text annotator loaded!")

    def login(self):
        try:
            login_status=self.client.login(self.username, self.password)
            if login_status:
                print("Logged in to Instagram successfully!")
                return 1
            else:
                print("Logged in to Instagram failed!")
            return 0

        except Exception as e:
            print(f"Error logging in: {e}")
            return 0

    def logoff(self):
        try:
            status = self.client.logout()
            print(f"Logged out of Instagram successfully! {status}")
            return 0
        except Exception as e:
            print(f"Error logging out: {e}")
            return 1
    def find_location(self, raw_location, default_city="Default"):
        Location = namedtuple("Location", ["name", "external_id", "lat", "lng"])

        try:
            lat = raw_location.get("lat", 0.01)
            lon = raw_location.get("lng", 0.01)
        except AttributeError:
            print(f"LOCATION: Invalid raw_location format: {raw_location}")
            lat, lon = 0.01, 0.01

        if lat == 0.01 or lon == 0.01:
            precise_lat, precise_lon = get_coordinates_from_name(default_city)
            lat, lon = randomize_coordinates(precise_lat, precise_lon, INSTAGRAM_DEFAULT_LOCATION_RANGE)

        locations = self.client.location_search(lat=round(lat, 8), lng=round(lon, 8))
        if not locations:
            print("LOCATION: No locations found.")
            return Location("Unknown", "0", lat, lon)

        closest_location = min(locations, key=lambda loc: haversine(lat, lon, loc.lat, loc.lng))
        print(f"LOCATION: Closest Location: Name: {closest_location.name}, ID: {closest_location.external_id}, "
              f"Lat: {closest_location.lat}, Lng: {closest_location.lng}")
        return closest_location

    def post_post(self, post):
        try:
            temp_image_path = f'D://2.dev//1.src//InstaPoster//images//temp_image_{post.image_name}.jpg'
            post.image.save(temp_image_path)

            post.location = self.find_location(post._raw_location, INSTAGRAM_DEFAULT_LOCATION)
            print("Location: ", post.location)

            picture_tags = self.google_image_analyzer.analyze_image(temp_image_path)
            picture_tags.extend(["traveling", post.location.name])
            print("Picture tags: ", picture_tags)

            selected_tags = random.sample(picture_tags, max(1, round(len(picture_tags) * 0.65)))
            print("Selected tags: ", selected_tags)

            prompt = (f"Create a short (less than 20 words) Instagram post based on tags {selected_tags}. use English letters only! Dont use word Embracing and Exploring and other fancy words in the beginning. Be natural and original.")
            description = self.openai_chat.chat(prompt)
            post.description = remove_first_and_last_from_str(description)
            print("Description: ", post.description)

            status = self.client.photo_upload(temp_image_path, caption=post.description, location=post.location)

            if status.media_type == 1:
                print("Photo uploaded successfully")
                return 1
            else:
                print("Upload completed, but post might not be visible.")
                return 0

        except Exception as e:
            print(f"Error while posting image: {e}")
            return 0

        finally:
            try:
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
                    print(f"Temporary image file {temp_image_path} removed successfully.")
            except Exception as cleanup_error:
                print(f"Error during cleanup: {cleanup_error}")



# Example usage:
if __name__ == "__main__":
    USERNAME = INSTAGRAM_USERNAME
    PASSWORD = INSTAGRAM_PASSWORD
    FOLDER_PATH = INSTAGRAM_IMAGE_FOLDER
    LOCATION = INSTAGRAM_DEFAULT_LOCATION

    # Schedule configuration: list of (start_time, end_time) in "HH:MM" format
    schedule_config = INSTAGRAM_POST_TIME_SLOTS

    # Random delay range between posts in seconds
    delay_range = INSTAGRAM_POST_DELAY_RANGE

    poster = Poster(USERNAME, PASSWORD)
    login_status=poster.login()
    if login_status == 0:
        print("Login failed")
        exit()

    iman = ImageManager(FOLDER_PATH)
    scheduler = Scheduler(schedule_config=schedule_config, delay_range=delay_range)

    i = 0
    for filename in os.listdir(FOLDER_PATH):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(FOLDER_PATH, filename)

            if iman.is_image_in_log(filename):
                print(f"File {filename} already posted")
                continue

            # Wait until within schedule
            while not scheduler.is_within_schedule():
               #if login_status == 1:
                    #login_status = poster.logoff()
                print("Waiting for the next available schedule...")
                time.sleep(300)  # Check every minute


            #if login_status == 0:
            #    login_status = poster.login()
            #    print("Log in...")
            #else:
            pic = Post(file_path)
            pic.resize_to_square()

            if i<INSTAGRAM_POST_LIMIT_PER_SLOT:
                status = poster.post_post(pic)
                if status:
                    iman.add_image_to_log(filename)
                    i = i + 1


            #print(f"login status {login_status}")
            # Wait for a randomized delay before posting the next image
            delay = scheduler.get_random_delay()
            print(f"Waiting for {delay} seconds before the next post...\n\n")
            time.sleep(delay)



    print("Posts created")
