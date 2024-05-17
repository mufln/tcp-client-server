from Crypto.Hash import keccak


def CheckPasswordHash(hash, password):
    checking = GeneratePasswordHash(password)
    return hash == checking


def GeneratePasswordHash(password):
    return keccak.new(digest_bits=512).update(password.encode("utf-8")).hexdigest()

