import base64
import requests

def get_b64_file(url: str):
    name = url.rsplit('/', maxsplit=1)[-1]
    content = base64.b64encode(requests.get(url).content).decode()
    return name, content
