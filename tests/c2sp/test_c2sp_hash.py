import pytest

from c2sp_vectors import ALL_KEM_DATA, KEM_IDS
from pyber.hash import G, H, J

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_G(kem_data):
    d = kem_data["d"]
    expected_rho = kem_data["rho"]
    expected_sigma = kem_data["sigma"]

    rho, sigma = G(d)

    assert rho == expected_rho
    assert sigma == expected_sigma

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_H(kem_data):
    ek = kem_data["ek"]
    expected_H_ek = kem_data["H_ek"]
    
    h = H(ek)
    
    assert h == expected_H_ek

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_J(kem_data):
    z = kem_data["z"]
    c = kem_data["c"]
    expected_K_bar = kem_data["K_bar"]
    
    K_bar = J(z + c)
    
    assert K_bar == expected_K_bar

# PRF is intrinsically tested by sample_poly_cbd