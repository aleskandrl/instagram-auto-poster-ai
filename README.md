# instagram-auto-poster-ai
 An automated Instagram posting tool with AI-generated captions and location tagging. Uses Instagrapi for posting and ChatGPT for smart descriptions based on image object detection via Google API

# Overview
InstaPoster is an automated tool designed to post images to Instagram. The program logs in to an Instagram account, analyzes images, generates descriptions using AI, and posts them at scheduled times. It integrates with Google's image analysis API for tag suggestions and OpenAI's GPT for generating captions, making posts more relevant and engaging.

# Features
- Instagram Login & Logout: Handles secure login and logout to the Instagram account using provided credentials.
- Image Uploading: Posts images from a specified folder to Instagram with relevant tags and captions.
- Location Finding: Uses coordinates to find the closest location for each post.
- Google Image Analyzer: Analyzes images to generate relevant tags.
- AI Caption Generation: Utilizes OpenAI's GPT-3 to generate short, natural-sounding captions based on image tags.
- Scheduling: Configures a posting schedule and waits until the next available time slot to post.
- Log Management: Keeps track of already posted images to avoid re-uploading them.

# File Structure
- poster.py: Main class for managing login, posting, and AI integrations.
- image_manager.py: Manages images in image folder.
- scheduler.py: Handles scheduling.

# Dependencies
- requests: To make HTTP requests for login and post actions.
- instabot: Instagram automation library for login and uploading.
- openai: For AI-driven caption generation.
- google-cloud-vision: For image analysis.
- time: For managing delays between posts.

# License
This project is licensed under the MIT License - see the LICENSE file for details.
