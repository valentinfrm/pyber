import pytest

from c2sp_vectors import ALL_KEM_DATA, KEM_IDS
from pyber.kem import _encaps_internal, _decaps_internal

# not testing keygen cause c2sp uses G(d), we need G(d||k) for FIPS 203

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_encaps_internal(kem_data):
    ek = kem_data["ek"]
    m = kem_data["m"]
    expected_K = kem_data["K"]
    expected_c = kem_data["c"]

    K, c = _encaps_internal(ek, m)

    assert K == expected_K
    assert c == expected_c

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_decaps_internal(kem_data):
    dk = kem_data["dkKEM"]
    c = kem_data["c"]
    expected_K = kem_data["K"]

    K = _decaps_internal(dk, c)

    assert K == expected_K
