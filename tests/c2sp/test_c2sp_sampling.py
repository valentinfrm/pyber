import pytest

from c2sp_vectors import ALL_KEM_DATA, KEM_IDS
from pyber.hash import PRF
from pyber import params
from pyber.sampling import expand, sample_poly_cbd

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True) # indirect -> send to fixture first
def test_expand(kem_data): # return of fixture
    rho = kem_data["rho"]
    A00 = kem_data["A00"]

    A = expand(rho)

    assert A00 == A[0][0].coeff

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_sample_poly_cbd(kem_data):
    sigma = kem_data["sigma"]
    expected_s0 = kem_data["s0"]

    prf_out = PRF(params.eta1, sigma, 0)
    s0 = sample_poly_cbd(prf_out, params.eta1)

    assert s0.coeff == expected_s0
    