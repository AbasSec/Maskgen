import string
import random
import re
import qrcode

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def is_valid_url(url):
    regex = re.compile(r'^https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return re.match(regex, url) is not None

def make_qr(data, filename):
    qr = qrcode.make(data)
    qr.save(filename)
    return filename
