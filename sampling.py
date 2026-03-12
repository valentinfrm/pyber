import params
import field
import polynomial
from Crypto.Hash import SHAKE128
from auxiliary import *

def sample_poly_cbd(byte_input, eta):
    """
    samples poly coeff from PRF output with CBD

    Args:
        b (bytes): 64 * eta byte array
        eta (int): {2,3}
    Returns:
        list: 256 coefficients in Zq
    """
    b = bytes_to_bits(byte_input)
    coeff = []

    for i in range(256):
        x = sum((b[2 * i * eta + j]) for j in range(eta))
        y = sum((b[2 * i * eta + eta + j]) for j in range(eta))
        coeff.append(field.reduce(x - y))

    return polynomial.poly(coeff)

def expand(rho):
    """
    in NTT realm
    """
    k = params.k
    A = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            A[i][j] = sample_NTT(rho + bytes([j]) + bytes([i]))
    return A


def sample_NTT(byte_input):
    shake = SHAKE128.new(byte_input)
    
    di = 0
    i = 0
    coeff = []

    while i < 256:
        C = shake.read(3) # 3 bytes -> 24 bits -> 2 * 12 (12 bits needed for max 3329)
        d1 = C[0] + 256 * (C[1] % 16)
        d2 = (C[1] >> 4) + 16 * C[2]

        # rejection sampling (if too high -> resample)
        if d1 < params.q and i < 256:
            coeff.append(d1)
            i += 1

        if d2 < params.q and i < 256:
            coeff.append(d2)
            i += 1
        
        di += 3

    return polynomial.poly(coeff)
