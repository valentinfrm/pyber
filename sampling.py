import params
import field
import hashlib
import polynomial
from auxiliary import *
import numpy as np

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

    return coeff

def expand(rho):
    k = params.k
    A = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            A[i][j] = sample_poly_shake(rho + bytes([j]) + bytes([i]))
    return A


def sample_poly_shake(byte_input):
    # problem -> no iterative squeezing
    # solution -> large enough pre calculated digest
    #               around (4096-3329)/4096 = 19% rejected -> on average 316 coeff needed -> 1000 bytes to make sure
    shake = hashlib.shake_128()
    shake.update(byte_input)
    byte_digest = shake.digest(1000)
    
    di = 0
    i = 0
    coeff = []

    while i < 256:
        bit_digest = bytes_to_bits(byte_digest[di:di+3]) # 3 bytes -> 24 bits -> 2 * 12 (12 bits needed for max 3329)
        c1 = sum((bit_digest[j]) * 2**j for j in range(12))
        c2 = sum((bit_digest[12 + j]) * 2**j for j in range(12))

        # rejection sampling (if too high -> resample)
        if c1 < params.q:
            coeff.append(c1)
            i = i + 1

        if c2 < params.q:
            coeff.append(c2)
            i = i + 1
        
        di = di + 3

    p = polynomial.poly(coeff)
    p.poly_reduce()
    return p