from argon2 import PasswordHasher


ph = PasswordHasher()


def hash_password(password: str):
    return ph.hash(password)


def validate_password(password: str, hashed_password: str):
    return ph.verify(hash=hashed_password, password=password)

