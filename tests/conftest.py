# pytest fixtures for ML-KEM parameterized tests
import pytest

from pyber import params

@pytest.fixture()
def kem_data(request):
    kem_data = request.param # gets data from parameter
    for key, value in kem_data["params"].items(): # sets params.key = value
        setattr(params, key, value)
    return kem_data