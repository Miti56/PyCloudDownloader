import requests
import json
from bs4 import BeautifulSoup
import os
import subprocess
import requests
import json
from bs4 import BeautifulSoup
import os
import subprocess
from mutagen.id3 import ID3, TPE1, TIT2, APIC
import shutil
import time

# coming from your soundcloud session.
cookie_string = "YOUR COOKIE"

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
        command = ["youtube-dl", "--no-check-certificate", "-x", "--audio-format", "mp3", soundcloud_url, "--cookies",
                   cookie_string]
        subprocess.run(command, check=True)
        print("Audio downloaded successfully.")

        # Fetch the specific .mp3 file
        mp3_file_to_edit = fetch_specific_mp3_file()

        if mp3_file_to_edit:
            # Add a delay to ensure the audio file is ready
            time.sleep(5)

            print("Embedding metadata and album cover...")

            # Open and embed album cover
            artwork_filename = "artwork/artwork.jpg"
            if os.path.exists(artwork_filename):
                audio = ID3(mp3_file_to_edit)
                artist, song_name = extract_metadata_from_json()
                print(f"Embedding Artist: {artist}")
                print(f"Embedding Song Name: {song_name}")
                audio.add(TPE1(encoding=3, text=artist))
                audio.add(TIT2(encoding=3, text=song_name))

                with open(artwork_filename, "rb") as img_file:
                    audio.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=img_file.read()))
                audio.save(mp3_file_to_edit)

                print("Metadata and album cover embedded.")

    except subprocess.CalledProcessError as e:
        print(f"Error during audio download: {e}")
    except Exception as e:
        print(f"Error during metadata embedding: {e}")


# Function to fetch the specific .mp3 file
def fetch_specific_mp3_file():
    files = os.listdir(os.getcwd())
    mp3_files = [file for file in files if file.endswith(".mp3")]

    if mp3_files:
        for mp3_file in mp3_files:
            mp3_file_path = os.path.join(os.getcwd(), mp3_file)
            try:
                # Try to open the file in read mode to check its validity
                audio = ID3(mp3_file_path)
                return mp3_file
            except Exception as e:
                # The file couldn't be opened in read mode, try to create a new valid ID3 tag
                try:
                    new_audio = ID3()
                    new_audio.save(mp3_file_path)
                    # Reopen in read-write mode for further operations
                    audio = ID3(mp3_file_path)
                    return mp3_file
                except Exception as e:
                    print(f"'{mp3_file}' could not be processed due to the error: {e}")

    print("No .mp3 files found to edit.")
    return None


# Function to check if a file is a valid MP3 file
def is_valid_mp3(file_path):
    try:
        audio = ID3(file_path)
        return True
    except Exception as e:
        print(f"'{file_path}' is not a valid MP3 file. Error: {e}")
        return False

# Function to remove unnecessary files created during runtime
def cleanup():
    try:
        # List of files to remove
        files_to_remove = ["soundcloud_html.json", "cookie", cookie_string, "artwork"]

        for file_name in files_to_remove:
            if os.path.exists(file_name):
                if os.path.isfile(file_name):
                    os.remove(file_name)
                elif os.path.isdir(file_name):
                    shutil.rmtree(file_name)

        print("Cleanup completed.")
    except Exception as e:
        print(f"Cleanup failed: {e}")


if __name__ == "__main__":
    soundcloud_url = input("Enter the SoundCloud URL: ")

    # Save the HTML content to JSON first
    save_html_to_json(soundcloud_url)

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

    # Extract metadata from JSON
    artist, song_name = extract_metadata_from_json()
    print(f"Artist: {artist}")
    print(f"Song Name: {song_name}")


    # Download audio after extracting metadata
    download_soundcloud_audio(soundcloud_url)

    cleanup()


