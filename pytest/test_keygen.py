from kyber_py.ml_kem import ML_KEM_768
import keygen

"""
def test_equal():
    d = bytes(32)
    z = bytes(32)
    x = keygen.pke_keygen(d)
    y = ML_KEM_768.key_derive(d + z)
    assert x[0] == y[0]  # ek
    assert x[1] == y[1]  # dk
"""