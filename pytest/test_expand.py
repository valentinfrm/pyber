import sampling
from kyber_py.kyber.kyber import Kyber
import params 

def test_expand():
    kyber_params = {
        "k": params.k,
        "eta_1": params.eta1,
        "eta_2": params.eta2,
        "du": params.du,
        "dv": params.dv
    }
    rho = bytes(range(32))

    my_A = sampling.expand(rho)

    kyber = Kyber(kyber_params)
    ref_A = kyber._generate_matrix_from_seed(rho, False)

    for i in range(params.k):
        for j in range(params.k):
            your_poly = my_A[i][j]
            ref_poly = ref_A._data[i][j]
            assert your_poly.coeff == ref_poly.coeffs