import subprocess

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
