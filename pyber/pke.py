import pyber.auxiliary as ax
from pyber.hash import G, PRF
from pyber.ntt import NTT, iNTT
from pyber import params
from pyber.polynomial import poly
from pyber.sampling import sample_poly_cbd, expand

#ek, dk PKE keys, not KEM encaps/decaps keys

def keygen(d):
    """
    generates public and private key

    Args:
        d (bytes): 32 byte random seed
    Returns:
        ek (bytes): encryption key -> coeff of t + rho
        dk (bytes): decryption key -> coeff of s
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

    # transform s into NTT
    s_hat = []
    for p in s:
        s_hat.append(poly(NTT(p.coeff)))

    # transform e into NTT
    e_hat = []
    for p in e:
        e_hat.append(poly(NTT(p.coeff)))

    # A * s
    As = []
    for row in range(params.k):
        p = poly([0] * params.n)
        for col in range(params.k):
            tmp = A[row][col] * s_hat[col]
            p += tmp
        As.append(p)

    # + e
    t_hat = []
    for row in range(params.k):
        t_hat.append(As[row] + e_hat[row])

    # takes all coeffs c from poly p for all polynomials in t/s
    t_hat_coeff = [c for p in t_hat for c in p.coeff]
    s_hat_coeff = [c for p in s_hat for c in p.coeff]

    # encode keys
    ek = ax.byte_encode(t_hat_coeff, 12) + rho
    dk = ax.byte_encode(s_hat_coeff, 12)

    return ek, dk

def encrypt(ek, m, r):
    """
    encrypts using the encryption key :)
    
    Args:
        ek (bytes): coeff of t + rho
        m (bytes): 32 byte message
        r (bytes): 32 byte random seed for PRF

    Returns:
        c (bytes): coeffs of u and v poly(s) -> (k * n * du + n * dv) / 8 bytes
    """
    rho = ek[-32:]
    t = ax.byte_decode(ek[:-32], 12)

    t_polys = [] # vector of length k with polynomials with n coeff
    for i in range(params.k):
        p = t[i * params.n:(i + 1) * params.n]
        t_polys.append(poly(p))
    
    A_T = ax.transpose_matrix(expand(rho))
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

    # transform y to NTT realm
    y_hat = []
    for p in y:
        y_hat.append(poly(NTT(p.coeff)))

    # u = (A_t * y) + e1
    u = [] # vector of polys length k
    for row in range(params.k):
        p = poly([0] * params.n) # poly with only 0s as coeff
        for col in range(params.k):
            p += A_T[row][col] * y_hat[col]
        p = poly(iNTT(p.coeff)) + e1[row]
        u.append(p)

    mu = poly(ax.decompress_poly(ax.byte_decode(m, 1), 1))
    
    # v = (t^T * y) + e2 + mu
    v = poly([0] * params.n) # just one poly because of dot product
    for i in range(params.k):
        v += (t_polys[i] * y_hat[i])
    v = poly(iNTT(v.coeff)) + e2 + mu
        
    c1 = b""
    for i in range(params.k):
        uc = ax.compress_poly(u[i].coeff, params.du)
        c1 += ax.byte_encode(uc, params.du)

    c2 = ax.byte_encode(ax.compress_poly(v.coeff, params.dv), params.dv)
    
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
        tmp = ax.byte_decode(c1[i * params.n * params.du // 8:(i + 1) * params.n * params.du // 8], params.du) # n coeff with du bits
        u.append(poly(ax.decompress_poly(tmp, params.du)))
    
    v = poly(ax.decompress_poly(ax.byte_decode(c2, params.dv), params.dv))

    s = []
    for i in range(params.k):
        tmp = ax.byte_decode(dk[i * params.n * 12 // 8:(i + 1) * params.n * 12 // 8], 12) # *12 because 12 bits per coeff
        s.append(poly(tmp))
    
    # s^T * u
    sT = poly([0] * params.n)
    for i in range(params.k):
        sT += (s[i] * poly(NTT(u[i].coeff))) # s already in NTT from dk
    
    w = v - poly(iNTT(sT.coeff))

    m = ax.byte_encode(ax.compress_poly(w.coeff, 1), 1)

    return m