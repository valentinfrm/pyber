import field
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
        x = sum((b[2 * i * eta + j]) for j in range(eta)) # wie for loop
        y = sum((b[2 * i * eta + eta + j]) for j in range(eta))
        coeff.append(field.reduce(x - y))

    return coeff
