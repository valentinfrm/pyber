import pytest

from c2sp_vectors import ALL_KEM_DATA, KEM_IDS
from pyber.pke import encrypt, decrypt

# not testing keygen cause c2sp uses G(d), we need G(d||k) for FIPS 203

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_pke_encrypt_768(kem_data):
    ek = kem_data["ek"]
    m = kem_data["m"]
    r = kem_data["r"]
    expected_c = kem_data["c"]
    
    c = encrypt(ek, m, r)

    assert c == expected_c

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_pke_decrypt(kem_data):
    c = kem_data["c"]
    dk = kem_data["dkPKE_NTT_s"]
    expected_m = kem_data["m"]

    m = decrypt(dk, c)

    assert m == expected_m