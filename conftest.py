# pytest configuration: adds root directory to Python path for module discovery
import params
import pytest

@pytest.fixture()
def set_kem_params(request):
    kem_data = request.param # gets data from parameter
    for key, value in kem_data["params"].items(): # sets params.key = value
        setattr(params, key, value)
    return kem_data