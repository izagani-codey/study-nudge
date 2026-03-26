from html.parser import HTMLParser
from urllib.request import Request, urlopen


class _VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._skip = False
        self._chunks = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"}:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            clean = data.strip()
            if clean:
                self._chunks.append(clean)

    def get_text(self):
        return " ".join(self._chunks)


def extract_text_from_url(url, timeout=15):
    req = Request(
        url,
        headers={
            "User-Agent": "StudyNudgeBot/1.0 (+https://local.study-nudge)"
        },
    )

    with urlopen(req, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type.lower():
            raise RuntimeError("URL did not return an HTML page.")

        raw_html = response.read().decode("utf-8", errors="ignore")

    parser = _VisibleTextParser()
    parser.feed(raw_html)
    return parser.get_text()
