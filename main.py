import os
import googleapiclient.discovery
from datetime import timedelta
import isodate

class YouTubePlaylistAnalyzer:
    def __init__(self):
        self.api_key = self.get_api_key()
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=self.api_key)

    def get_api_key(self):
        api_key_file = 'api_key.txt'
        if not os.path.exists(api_key_file):
            api_key = input("Enter your Google Cloud Console YouTube API key: ")
            with open(api_key_file, 'w') as file:
                file.write(api_key)
        else:
            with open(api_key_file, 'r') as file:
                api_key = file.read().strip()
        return api_key

    def get_playlist_info(self, playlist_id):
        request = self.youtube.playlists().list(
            part="snippet,contentDetails",
            id=playlist_id
        )
        response = request.execute()
        if "items" not in response or not response["items"]:
            raise ValueError("Invalid playlist ID or playlist not found")

        playlist_info = response['items'][0]
        return playlist_info

    def get_playlist_videos(self, playlist_id):
        request = self.youtube.playlistItems().list(
            part="contentDetails,snippet",
            playlistId=playlist_id,
            maxResults=50
        )

        videos = []
        while request:
            response = request.execute()
            videos += response['items']
            request = self.youtube.playlistItems().list_next(request, response)
        
        return videos

    def get_video_durations(self, video_ids):
        durations = []
        for i in range(0, len(video_ids), 50):
            request = self.youtube.videos().list(
                part="contentDetails,snippet",
                id=",".join(video_ids[i:i+50])
            )
            response = request.execute()
            durations += [(item['contentDetails']['duration'], item['snippet']['title']) for item in response['items']]
        
        return durations

    @staticmethod
    def iso8601_duration_to_seconds(duration):
        duration = isodate.parse_duration(duration)
        return int(duration.total_seconds())

    @staticmethod
    def format_duration(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"

    def get_playlist_total_duration(self, playlist_url):
        playlist_id = playlist_url.split("list=")[1].split("&")[0]

        playlist_info = self.get_playlist_info(playlist_id)
        playlist_title = playlist_info['snippet']['title']
        video_count = playlist_info['contentDetails']['itemCount']

        print(f"Playlist Title: {playlist_title}")
        print(f"Total Videos: {video_count}")

        videos = self.get_playlist_videos(playlist_id)

        video_ids = [video['contentDetails']['videoId'] for video in videos]

        durations_and_titles = self.get_video_durations(video_ids)

        total_seconds = 0
        for duration, title in durations_and_titles:
            seconds = self.iso8601_duration_to_seconds(duration)
            total_seconds += seconds
            #print(f"Video Title: {title} | Duration: {self.format_duration(seconds)}")

        total_duration = self.format_duration(total_seconds)
        
        return total_duration


if __name__ == "__main__":
    analyzer = YouTubePlaylistAnalyzer()
    playlist_url = input("Enter playlist URL: ")
    total_duration = analyzer.get_playlist_total_duration(playlist_url)
    print(f"Total duration of the playlist: {total_duration}")
