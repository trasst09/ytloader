"""Local web form for ytloader: paste a playlist link, get mp3s."""
import html
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

from ytloader import download_playlist

PAGE = """<!doctype html>
<title>ytloader</title>
<h1>YouTube playlist to MP3</h1>
<form method="post" action="/download">
  <input name="url" type="url" placeholder="Playlist URL" size="60" required>
  <button type="submit">Download</button>
</form>
<p>{message}</p>
"""


class Handler(BaseHTTPRequestHandler):
    def _respond(self, message=""):
        body = PAGE.format(message=html.escape(message)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._respond()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        fields = parse_qs(self.rfile.read(length).decode())
        url = fields.get("url", [""])[0].strip()
        if url:
            threading.Thread(target=download_playlist, args=(url,), daemon=True).start()
            self._respond(f"Started downloading: {url}. Files land in downloads/, check the terminal for progress.")
        else:
            self._respond("Please enter a URL.")


if __name__ == "__main__":
    port = 8000
    print(f"Open http://localhost:{port} in your browser")
    ThreadingHTTPServer(("localhost", port), Handler).serve_forever()
