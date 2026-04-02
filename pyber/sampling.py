from Crypto.Hash import SHAKE128

from pyber import params
from pyber.polynomial import poly

def sample_poly_cbd(byte_input, eta):
    """
    samples a polynomial using the centered binomial distribution (CBD)

    Args:
        b (bytes): 64 * eta byte array
        eta (int): {2,3}
    Returns:
        poly: polynomial with 256 coeffs in Zq
    """

    int_input = int.from_bytes(byte_input, "little")
    coeffs = [0] * 256

    m1 = (1 << eta) - 1 # for eta = 2: 11b -> two bits
    m2 = (1 << 2 * eta) - 1 # total amount needed

    for i in range(256):
        tmp = int_input & m2
        x = (tmp & m1).bit_count() # bitcount == manual sum with loop
        y = ((tmp >> eta) & m1).bit_count()
        coeffs[i] = (x - y) % params.q

        int_input >>= 2 * eta # cuts used ones off

    return poly(coeffs)

def expand(rho):
    """
    samples a k x k matrix of polynomials in the NTT domain

    Args:
        rho (bytes): 32 byte seed
    """

    k = params.k
    A = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            A[i][j] = sample_NTT(rho + bytes([j]) + bytes([i]))
    return A

def sample_NTT(byte_input):
    """
    Samples a polynomial directly in the NTT domain using rejection sampling
    coeffs are generated with SHAKE128
    """
    
    shake = SHAKE128.new(byte_input)
    all_bytes = shake.read(840)

    i = 0
    coeff = [0] * 256
    pos = 0

    while i < 256 and pos + 3 <= len(all_bytes):
        c_bytes = all_bytes[pos:pos+3]
        pos += 3

        c_int = int.from_bytes(c_bytes, "little") # little -> d1 d2 d3 d4 d5 stream from shake

        d1 = c_int & 0xFFF # bottom 12 Bits
        d2 = (c_int >> 12) & 0xFFF

        # rejection sampling (if too high -> resample)
        if d1 < params.q and i < 256:
            coeff[i] = d1
            i += 1

        if d2 < params.q and i < 256:
            coeff[i] = d2
            i += 1

    return poly(coeff)
