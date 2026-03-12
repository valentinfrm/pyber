import sampling
import params
from kyber_py.polynomials.polynomials import PolynomialRing
import sampling

def test_sample_poly_shake():
    result = sampling.sample_NTT(bytes(32) + bytes([0]) + bytes([0]))
    assert len(result.coeff) == 256
    assert all(0 <= c < params.q for c in result.coeff)

def test_sample_poly_cbd_simple():
    test_input = bytes(range(128))
    eta = 2
    
    your_result = sampling.sample_poly_cbd(test_input, eta)
    
    R = PolynomialRing()
    ref_result = R.cbd(test_input, eta)
    
    assert your_result.coeff == list(ref_result)
