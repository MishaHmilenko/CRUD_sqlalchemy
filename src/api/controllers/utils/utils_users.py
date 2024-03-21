import hashlib
import random
import string


async def get_random_string(length=12):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


async def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = await get_random_string()
    enc = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode(), 100_000)
    return enc.hex()


async def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split('$')
    return await hash_password(password, salt) == hashed

