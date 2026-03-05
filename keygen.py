from hash import G,PRF
from polynomial import poly
import os
import params
import sampling
import auxiliary

def pke_keygen(d):
    """
    generates public and private key

    Args:
        d (bytes): 32 byte random seed
    Returns:
        ek (list): public encapsulation key
        dk (list): private decapsulation key
    """

    rho, sigma = G(d + bytes([params.k]))
    A = sampling.expand(rho)
    N = 0

    # generate s
    s = []
    for _ in range(params.k):
        s.append(sampling.sample_poly_cbd(PRF(params.eta1, sigma, N), params.eta1))
        N += 1

    #generate e
    e = []
    for _ in range(params.k):
        e.append(sampling.sample_poly_cbd(PRF(params.eta1, sigma, N), params.eta1))
        N += 1

    # A * s
    As = []
    for row in range(params.k):
        p = poly([0] * params.n)
        for col in range(params.k):
            tmp = A[row][col] * s[col]
            p += tmp
        As.append(p)

    # + e
    t = []
    for row in range(params.k):
        t.append(As[row] + e[row])

    # takes all coeffs c from poly p for all polynomials in t/s
    t_coeff = [c for p in t for c in p.coeff]
    s_coeff = [c for p in s for c in p.coeff]

    # encode keys
    ek = auxiliary.byte_encode(12, t_coeff) + rho
    dk = auxiliary.byte_encode(12, s_coeff)

    return (ek, dk)
    
    