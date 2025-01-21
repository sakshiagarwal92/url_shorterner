import hashlib

def generate_short_url(original_url):
    hash_object = hashlib.md5(original_url.encode())
    return hash_object.hexdigest()[:6]
