import requests
import json
from bs4 import BeautifulSoup
import os
import subprocess

# Function to extract and format the artist name
def format_artist_name(title):
    # Split the title at the "by" keyword and remove extra text
    parts = title.split(" by ")
    if len(parts) > 1:
        artist = parts[1]
        artist = artist.split(" | Listen online for free on SoundCloud")[0]
        return artist.strip()
    else:
        return "Unknown"

# Function to extract and format the song name
def format_song_name(title):
    # Split the title by "STREAM" and "by" and keep the part in between
    parts = title.split(" by ")
    if len(parts) > 1:
        song_name = parts[0].replace("Stream", "").strip()
        # Remove mentions of "(Free Download)" with case-insensitive handling
        song_name = song_name.replace("(Free Download)", "").replace("(FREE DOWNLOAD)", "").strip()
        return song_name.strip()
    else:
        return title  # Fallback to the original title if no "by" is found

# Function to save the HTML content to a JSON file
def save_html_to_json(url):
    try:
        # Send an HTTP GET request to the SoundCloud URL
        response = requests.get(url)
        response.raise_for_status()

        # Save the HTML content to a JSON file
        with open("soundcloud_html.json", "w", encoding="utf-8") as json_file:
            json.dump({"html_content": response.text}, json_file, ensure_ascii=False, indent=4)

        print("HTML content saved to soundcloud_html.json")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Function to parse and extract metadata
def extract_metadata_from_json():
    with open("soundcloud_html.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        html_content = data.get("html_content", "")

        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.text

            # Format and extract the artist and song name
            artist = format_artist_name(title)
            song_name = format_song_name(title)

            # # Extract the publication date
            # date_tag = soup.find('time', {"pubdate": True})
            # if date_tag:
            #     publication_date = date_tag['pubdate']
            #     print(publication_date)
            # else:
            #     publication_date = "Unknown"

            return artist, song_name

# Function to download the artwork
def download_artwork(url, output_folder="artwork"):
    try:
        # Send an HTTP GET request to the artwork URL
        response = requests.get(url)
        response.raise_for_status()

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Save the artwork to the output folder
        artwork_filename = os.path.join(output_folder, "artwork.jpg")
        with open(artwork_filename, "wb") as artwork_file:
            artwork_file.write(response.content)

        print(f"Artwork downloaded and saved as {artwork_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def download_soundcloud_audio(soundcloud_url):

    try:
        cookies = "2-294401-177040666-Heo0hHuZCIcnar"
        command = ["youtube-dl","--no-check-certificate" ,"-x", "--audio-format", "mp3", soundcloud_url, "--cookies", cookies]
        subprocess.run(command, check=True)
        print("Audio downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    soundcloud_url = input("Enter the SoundCloud URL: ")
    download_soundcloud_audio(soundcloud_url)
    save_html_to_json(soundcloud_url)

    artist, song_name = extract_metadata_from_json()
    print(f"Artist: {artist}")
    print(f"Song Name: {song_name}")


    # Extract the artwork URL from the JSON content
    with open("soundcloud_html.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        html_content = data.get("html_content", "")

        soup = BeautifulSoup(html_content, 'html.parser')
        meta_tags = soup.find_all('meta')
        for meta_tag in meta_tags:
            if 'property' in meta_tag.attrs and 'og:image' in meta_tag['property']:
                artwork_url = meta_tag['content']
                break

    if artwork_url:
        download_artwork(artwork_url)
