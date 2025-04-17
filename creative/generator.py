from openai import OpenAI
from tempfile import NamedTemporaryFile
from base64 import b64decode

client = OpenAI()

def gen_square(prompt: str) -> bytes:
    rsp = client.images.generate(prompt=prompt, size="512x512", n=1, response_format="b64_json")
    img_b64 = rsp.data[0].b64_json
    return b64decode(img_b64)
