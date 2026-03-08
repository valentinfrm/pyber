from hash import G, PRF
from sampling import sample_poly_cbd, expand
from polynomial import poly
import params
import auxiliary

#ek, dk PKE keys, not KEM encaps/decaps keys

def pke_keygen(d):
    """
    generates public and private key

    Args:
        d (bytes): 32 byte random seed
    Returns:
        ek (list): encryption key -> coeff of t + rho
        dk (list): decryption key -> coeff of s
    """

    rho, sigma = G(d + bytes([params.k]))
    A = expand(rho)
    N = 0

    # generate s
    s = []
    for _ in range(params.k):
        s.append(sample_poly_cbd(PRF(params.eta1, sigma, N), params.eta1))
        N += 1

    #generate e
    e = []
    for _ in range(params.k):
        e.append(sample_poly_cbd(PRF(params.eta1, sigma, N), params.eta1))
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
    ek = auxiliary.byte_encode(t_coeff, 12) + rho
    dk = auxiliary.byte_encode(s_coeff, 12)

    return (ek, dk)

def encrypt(ek, m, r):
    """
    encrypts a message using the encryption key :)
    
    Args:
        ek (bytes): coeff of t + rho
        m (bytes): 32 byte message
        r (bytes): 32 byte random seed for PRF

    Returns:
        c (bytes): coeffs of u and v poly(s) -> (k * n * du + n * dv) / 8 bytes
    """
    rho = ek[-32:]
    t = auxiliary.byte_decode(ek[:-32], 12)

    t_polys = [] # vector of length k with polynomials with n coeff
    for i in range(params.k):
        p = t[i * params.n:(i + 1) * params.n]
        t_polys.append(poly(p))
    
    A_T = auxiliary.transpose_matrix(expand(rho))
    N = 0
    
    # sample y vector
    y = []
    for _ in range(params.k):
        y.append(sample_poly_cbd(PRF(params.eta1, r, N), params.eta1))
        N += 1

    # sample e1 vector
    e1 = []
    for _ in range(params.k):
        e1.append(sample_poly_cbd(PRF(params.eta2, r, N), params.eta2))
        N += 1

    # sample e2 polynomial
    e2 = sample_poly_cbd(PRF(params.eta2, r, N), params.eta2)

    # u = (A_t * y) + e1
    u = [] # vector of polys length k
    for row in range(params.k):
        p = poly([0] * params.n) # poly with only 0s as coeff
        for col in range(params.k):
            p += A_T[row][col] * y[col]
        p += e1[row]
        u.append(p)

    mu = poly(auxiliary.decompress_poly(auxiliary.byte_decode(m, 1), 1))
    
    # v = (t^T * y) + e2 + mu
    v = poly([0] * params.n) # just one poly because of dot product
    for i in range(params.k):
        v += (t_polys[i] * y[i])
    v += e2
    v += mu
        
    c1 = b""
    for i in range(params.k):
        uc = auxiliary.compress_poly(u[i].coeff, params.du)
        c1 += auxiliary.byte_encode(uc, params.du)

    c2 = auxiliary.byte_encode(auxiliary.compress_poly(v.coeff, params.dv), params.dv)
    
    return c1 + c2

def decrypt(dk, c):
    """
    decrypts the ciphertext to retrieve the message
    by retrieving polys + calculating v - (s^T * u)
    
    Args:
        dk (list): coeffs of k polys appended -> k * n * 12 / 8 bytes
        c (bytes): coeffs of u and v poly(s) -> (k * n * du + n * dv) / 8 bytes

    Returns:
        m (bytes): decrypted 32 byte message
    """
    c1 = c[0:32*params.du*params.k]
    c2 = c[32*params.du*params.k:]

    u = []
    for i in range(params.k):
        tmp = auxiliary.byte_decode(c1[i * params.n * params.du // 8:(i + 1) * params.n * params.du // 8], params.du) # n coeff with du bits
        u.append(poly(auxiliary.decompress_poly(tmp, params.du)))
    
    v = poly(auxiliary.decompress_poly(auxiliary.byte_decode(c2, params.dv), params.dv))

    s = []
    for i in range(params.k):
        tmp = auxiliary.byte_decode(dk[i * params.n * 12 // 8:(i + 1) * params.n * 12 // 8], 12) # *12 because 12 bits per coeff
        s.append(poly(tmp))
    
    # s^T * u
    sT = poly([0] * params.n)
    for i in range(params.k):
        sT += (s[i] * u[i])
    
    w = v - sT

    m = auxiliary.byte_encode(auxiliary.compress_poly(w.coeff, 1), 1)

    return m