from ntt import NTT, iNTT

def test_reversable():
    f = list(range(256))
    f_test = iNTT(NTT(f))
    assert f == f_test