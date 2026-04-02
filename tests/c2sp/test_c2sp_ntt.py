import pytest

from c2sp_vectors import ALL_KEM_DATA, KEM_IDS
from pyber.ntt import NTT, iNTT

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_ntt_s0_768(kem_data):
    s0 = kem_data["s0"]
    expected_ntt_s0 = kem_data["NTT_s0"]

    ntt_s0 = NTT(s0)

    assert ntt_s0 == expected_ntt_s0

@pytest.mark.parametrize("kem_data", ALL_KEM_DATA, ids=KEM_IDS, indirect=True)
def test_iNTT_s0_768(kem_data):
    ntt_s0 = kem_data["NTT_s0"]
    expected_s0 = kem_data["s0"]

    s0 = iNTT(ntt_s0)
    
    assert s0 == expected_s0
