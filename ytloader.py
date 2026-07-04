"""Download every video in a YouTube playlist as an mp3."""
import sys
import yt_dlp


def download_playlist(url: str, out_dir: str = "downloads") -> None:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{out_dir}/%(playlist_title)s/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "ignoreerrors": True,  # skip unavailable videos instead of aborting the whole playlist
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    playlist_url = sys.argv[1] if len(sys.argv) > 1 else input("Playlist URL: ").strip()
    download_playlist(playlist_url)
