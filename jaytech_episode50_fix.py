"""
The Jaytech Music Podcast Episode 50 file on PodBean is broken:
  - There are extra bytes at the start of the file that are HTML content
  - The remaining file content is an m4a file, not an mp3
  
This script downloads and fixes the Podcast episode.

Episode link: https://jaytechmusic.podbean.com/e/jaytech-music-podcast-050/

The file will be saved in the directory where the script is run as:
  "Jaytech_Music_Podcast_050.m4a"
  
Broken file signature:
  MD5:  ca40ec3ae2e4676ea74218eae8dec8bb  shows_jaytech-music-podcast_audioposts_562476.mp3
  SHA1: 26289241688a9f974bc140b872734dab05fe6638  shows_jaytech-music-podcast_audioposts_562476.mp3
"""

import requests

r = requests.get('https://mcdn.podbean.com/mf/download/y7gqjq/shows_jaytech-music-podcast_audioposts_562476.mp3')
with open("Jaytech_Music_Podcast_050.m4a", 'wb') as outfile:
	outfile.write(r.content[969:])

# As an alternative, if you have already downloaded the file, comment the lines above and use the following:
#with open('shows_jaytech-music-podcast_audioposts_562476.mp3', 'rb') as infile:
#	r = infile.read()
#with open("Jaytech_Music_Podcast_050.m4a", 'wb') as outfile:
#	outfile.write(r.content[969:])	
