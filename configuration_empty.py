INSTAGRAM_USERNAME="alex_khristoforov"
INSTAGRAM_PASSWORD=""

INSTAGRAM_IMAGE_FOLDER="D://2.dev//1.src//InstaPoster//images"
INSTAGRAM_DEFAULT_LOCATION="Tbilisi"
INSTAGRAM_DEFAULT_LOCATION_RANGE=20

INSTAGRAM_POST_DELAY_RANGE = (150, 350)   # Random delay range between posts in seconds
INSTAGRAM_POST_TIME_SLOTS = [  # Schedule configuration: list of (start_time, end_time) in "HH:MM" format
        ("02:40", "03:31"),
        ("08:14", "10:01"),
        ("10:14", "11:25"),
        ("15:00",  "16:01"),
        ("19:00",  "20:00"),
        ("01:15",  "02:00"),
        ("02:30",  "02:55")
    ]
INSTAGRAM_POST_LIMIT_PER_SLOT = 15

USE_AI=True
GOOGLE_CREDENTIALS_PASS = ".json"
OPENAI_API_KEY=""
OPENAI_API_SETTINGS = {
    "model": "gpt-4",
    "role": "You are very creative SMM",
    "max_tokens": 100,      # Adjust the response length
    "temperature": 0.9,     # Adjust creativity (0.0-1.0)
    "n": 1                  # Number of responses
}
