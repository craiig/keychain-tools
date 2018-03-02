import hashlib

def util_hash(hash_object, file_path):
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_object.update(chunk)
    return hash_object.hexdigest()

def util_sha256_hash(file_path):
    return util_hash(hashlib.sha256(), file_path)
