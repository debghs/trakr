# trakr

A Python script to analyze an YouTube playlist and calculate the total duration of all videos in the playlist.

## Features

- Fetch playlist information including title and total number of videos.
- Calculate the total duration of all videos in the playlist.

## Prerequisites

- Python 3.6+
- Google API Client Library for Python
- `isodate` library

## Installation

1. **Clone the repository:**

   - ```git clone https://github.com/yourusername/YouTubePlaylistAnalyzer.git```
   - ```cd YouTubePlaylistAnalyzer```
  
2. Install required libraries:

    ```pip install google-api-python-client isodate```

3. Get a YouTube Data API Key:

  - Go to the Google Cloud Console.
  - Create a new project.
  - Enable the ```YouTube Data API v3 for your``` project.
  - Create an API key.

# Usage

1. Run the script:
  ```python YouTubePlaylistAnalyzer.py```
  
2. Enter your Google Cloud Console YouTube API key when prompted.

3. Enter the playlist URL when prompted.
