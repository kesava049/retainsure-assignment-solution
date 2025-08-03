# app/models.py

import threading
from datetime import datetime, timezone

class URLStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.urls = {}  # short_code -> metadata dict

    def create_short_url(self, short_code, original_url):
        with self.lock:
            self.urls[short_code] = {
                "url": original_url,
                "clicks": 0,
                "created_at": datetime.now(timezone.utc).isoformat()
            }

    def get_url(self, short_code):
        with self.lock:
            return self.urls.get(short_code)

    def increment_click(self, short_code):
        with self.lock:
            if short_code in self.urls:
                self.urls[short_code]["clicks"] += 1

    def short_code_exists(self, short_code):
        with self.lock:
            return short_code in self.urls
