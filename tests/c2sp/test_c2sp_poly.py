import pytest

from c2sp_vectors import ALL_KEM_DATA, KEM_IDS
from pyber.auxiliary import byte_decode, byte_encode
from pyber.ntt import NTT
from pyber import params
from pyber.polynomial import poly

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_poly_mul(kem_data):
    A_bytes = kem_data["A"]

    poly_len = 384
    k = params.k

    A = []
    for i in range(k):
        row = []
        for j in range(k):
            start = (i * k + j) * poly_len
            poly_coeffs = byte_decode(A_bytes[start:start+poly_len], 12)
            row.append(poly(poly_coeffs))
        A.append(row)
    
    s_bytes = kem_data["s"]
    s_hat = []
    for i in range(k):
        start = i * poly_len
        s_coeffs = byte_decode(s_bytes[start:start + poly_len], 12)
        s_hat.append(poly(NTT(s_coeffs)))

    e_bytes = kem_data["e"]
    e_hat = []
    for i in range(k):
        start = i * poly_len
        e_coeffs = byte_decode(e_bytes[start:start + poly_len], 12)
        e_hat.append(poly(NTT(e_coeffs)))

    # A * s
    As = []
    for row in range(k):
        p = poly([0] * 256)
        for col in range(k):
            tmp = A[row][col] * s_hat[col]
            p += tmp
        As.append(p)

    # + e
    t_hat = []
    for row in range(k):
        t_hat.append(As[row] + e_hat[row])

    t_hat_coeff = [c for p in t_hat for c in p.coeff]
    t_hat_bytes = byte_encode(t_hat_coeff, 12)

    expected_t_bytes = kem_data["t"]
    
    assert t_hat_bytes == expected_t_bytes

def test_poly_add():
    a = [3328, 1, 0, 2000]
    b = [2, 3328, 1, 2000]
    expected = [1, 0, 1, 671]

    polyResult = poly(a) + poly(b)
    assert expected == polyResult.coeff

def test_poly_sub():
    a = [3328, 1, 0, 2000]
    b = [2, 3328, 1, 2000]
    expected = [3326, 2, 3328, 0]

    polyResult = poly(a) - poly(b)
    assert expected == polyResult.coeff 

def test_poly_reduce():
    input = [5000, 10000, 15000, 20000]
    expected = [1671, 13, 1684, 26]
    polyI = poly(input)
    polyI.poly_reduce()
    assert expected == polyI.coeff