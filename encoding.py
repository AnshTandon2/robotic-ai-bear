import base64
from pathlib import Path

def encode_data(filepath: Path) -> str:

    with Path(filepath).open('rb') as fp:
        bytes_data = base64.b64encode(fp.read())
        encoded_data = bytes_data.decode("utf-8")
        return encoded_data

filepath = "WIN_20240330_11_59_42_Pro.mp4"
encoded_data = encode_data(filepath)
print(encoded_data)


