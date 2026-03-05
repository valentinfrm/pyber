from polynomial import poly
"""change q = 41 in params
def test_poly_mul():
    p1 = poly([23, 0, 11, 7])
    p2 = poly([40, 5, 16, 0])
    result = p1.poly_mul(p2)
    assert result.coeff == [12, 3, 29, 7]
"""

def test_poly_mul_kyber():
    from kyber_py.polynomials.polynomials_generic import GenericPolynomialRing
    R = GenericPolynomialRing(3329, 256)
    coeffs1 = list(range(256))
    coeffs2 = list(range(256, 512))
    f = R(coeffs1)
    g = R(coeffs2)
    expected = list((f * g).coeffs)
    p1 = poly(coeffs1)
    p2 = poly(coeffs2)
    result = p1 * p2
    assert result.coeff == expected
