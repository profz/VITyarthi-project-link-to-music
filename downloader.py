import yt_dlp
import os
import re
import sys


class Converter:

    def __init__(self):
        self.dir = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(self.dir, exist_ok=True)

        self.formats = {
            'mp3': 'mp3',
            'wav': 'wav',
            'aac': 'm4a',
            'flac': 'flac',
            'ogg': 'opus',
            'm4a': 'm4a'
        }

    def valid_url(self, url):
        pattern = r'(https?://)?(www\.|m\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)[\w-]+'
        return bool(re.match(pattern, url))

    def download(self, url, format='mp3'):
        if not self.valid_url(url):
            print("Invalid YouTube URL")
            return False

        if format not in self.formats:
            print(f"unsupported format, Use : {
                  ', '.join(self.formats.keys())} ")
            return False

        print(f"Downloading and converting your music to {format.upper()}!")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.dir}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.formats[format],
                'preferredquality': '192',
            }],
            'quiet': False,
            'no_warnings': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')
                print(f"\n Done! Audio Saved as: {title}.{format}")
                print(f" Location: {self.dir}")
                return True

        except Exception as e:
            print(f"\n Met with Error: {str(e)}")
            return False


def main():

    if len(sys.argv) < 2:
        print("YouTube Audio Converter")
        print("\n Usage:")
        print("python downloader.py <youtube_url> [format]")
        print("\n These are the Examples:")
        print("python downloader.py https://youtube.com/watch?v=... mp3")
        print("python downloader.py https://youtu.be/... wav")
        print("\n Please Use The Supported formats: mp3, wav, aac, flac, ogg, m4a")
        print("Default format: mp3")
        print("If any doubts please contact https://github.com/profz.com ")
        sys.exit(1)

    url = sys.argv[1]
    format = sys.argv[2].lower() if len(sys.argv) > 2 else 'mp3'

    conv = Converter()
    success = conv.download(url, format)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
