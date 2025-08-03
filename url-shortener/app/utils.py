# app/utils.py

import random
import re

SHORT_CODE_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
SHORT_CODE_LENGTH = 6

def generate_short_code(existing_codes):
    for _ in range(10):
        code = ''.join(random.choices(SHORT_CODE_CHARS, k=SHORT_CODE_LENGTH))
        if code not in existing_codes:
            return code
    raise Exception("Unable to generate unique short code after 10 attempts")

def is_valid_url(url):
    # Accept http:// or https:// with at least one "." later
    regex = re.compile(
        r"^(https?://)"           # http:// or https:// required
        r"([\w\-]+\.)+[\w\-]+"    # at least one ".", domain part
        r"([/?#][^\s]*)?$",       # optional path/query/hash
        re.IGNORECASE
    )
    return re.match(regex, url) is not None
