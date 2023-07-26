import json
import base64
import re

def encode_text(text):
    encoded_text = base64.b64encode(text.encode()).decode()
    return encoded_text

def decode_text(encode_text):
    decoded_text = base64.b64decode(encode_text).decode()
    return decoded_text

def is_obfuscated(text):
    # Define regular expression pattern for obfuscated Base64
    pattern = r"^[A-Za-z0-9+/]{2,}[=]{0,2}$"
    # Check if the text matches the pattern
    if re.match(pattern, text):
        try:
            # Try decoding the text as Base64
            base64_decoded = base64.b64decode(text)
            # Check if the decoded text is valid UTF-8
            base64_decoded.decode('utf-8')
            # The text is likely obfuscated Base64
            return True
        except (base64.binascii.Error, UnicodeDecodeError):
            pass
    # The text is not obfuscated Base64
    return False
