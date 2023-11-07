# PyCloudDownloader
 
# SoundCloud Audio Downloader with Metadata Embedding

This Python script allows you to download audio from SoundCloud, embed metadata (artist and song name), and album cover artwork into the downloaded MP3 file.

## Capabilities

- Download audio from SoundCloud as MP3.
- Extract and format the artist name and song name.
- Embed artist, song name, and album cover artwork into the downloaded MP3 file.
- Cleanup temporary files created during runtime.

## Requirements

To run this script, you need the following:

- Python 3.x
- `requests` library (can be installed using `pip install requests`)
- `beautifulsoup4` library (can be installed using `pip install beautifulsoup4`)
- `mutagen` library (can be installed using `pip install mutagen`)
- `youtube-dl` command-line tool

Make sure you have these dependencies installed before using the script.

## Installation

1. Clone the repository or download the script to your local machine.

2. Install the required Python libraries (requests, beautifulsoup4, and mutagen) using `pip`:

   ```bash
   pip install requests beautifulsoup4 mutagen

3. Install youtube-dl by following the installation instructions on their official website: https://github.com/ytdl-org/youtube-dl#installation

# How to Get the Cookie

In order to download audio from SoundCloud, you need to obtain a valid SoundCloud session cookie. Follow these steps to obtain your SoundCloud session cookie:

Open your web browser and visit SoundCloud (https://soundcloud.com).
Log in to your SoundCloud account.
After logging in, access your browser's developer tools:
For Google Chrome, press F12 or Ctrl+Shift+I.
For Mozilla Firefox, press F12 or Ctrl+Shift+I.
Go to the "Application" or "Storage" tab in the developer tools (the name may vary depending on your browser).
In the left sidebar, you'll see "Cookies" or "Local Storage." Click on it.
Find the SoundCloud cookie named session and copy its value. This is your session cookie.

# How to Use

1. Run the script using Python:

```
python soundcloud_downloader.py
```


2. When prompted, enter the SoundCloud URL of the track you want to download.
3. The script will download the audio, extract metadata, and embed it into the MP3 file, along with the album cover artwork.
4. The resulting MP3 file will be named according to the song's title.
5. After the process is complete, you can find the downloaded audio in the same directory as the script.

# Enjoy your music downloads!