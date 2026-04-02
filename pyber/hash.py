import hashlib

def PRF(eta, s, ctr):
    """ 
    pseudorandom function to generate noise

    Args:
        eta (int): {2,3}
        s (bytes): 32 Byte seed
        ctr (int): int ctr to use seed multiple times

    Returns:
        bytes: 64 * eta Bytes noise
    """
    shake = hashlib.shake_256()
    shake.update(s + bytes([ctr]))
    return shake.digest(64 * eta) # Takes length in byte

def H(s):
    """
    Args:
        s (bytes): variable-length input

    Returns:
        bytes: 32 Byte digest
    """
    hash = hashlib.sha3_256()
    hash.update(s)
    return hash.digest()

def J(s):
    """
    Args:
        s (bytes): variable-length input

    Returns:
        bytes: 32 Byte digest
    """
    shake = hashlib.shake_256()
    shake.update(s)
    return shake.digest(32) # Takes length in byte

def G(c):
    """
    Args:
        c (bytes): variable-length input

    Returns:
        a: 32 Byte
        b: 32 Byte
        where G(c) = a || b
    """
    hash = hashlib.sha3_512()
    hash.update(c)
    digest_combined = hash.digest()
    a = digest_combined[:32]
    b = digest_combined[32:]
    return a,b