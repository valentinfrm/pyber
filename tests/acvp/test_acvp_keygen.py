import json

from kyber_py.ml_kem import ML_KEM_512

from pyber.hash import PRF, G
from pyber import kem
from pyber.ntt import NTT
from pyber import params
from pyber.sampling import sample_poly_cbd

k_map = {
    "ML-KEM-512":  {"k": 2, "eta1": 3, "du": 10, "dv": 4},
    "ML-KEM-768":  {"k": 3, "eta1": 2, "du": 10, "dv": 4},
    "ML-KEM-1024": {"k": 4, "eta1": 2, "du": 11, "dv": 5},
}

with open("tests/acvp/keygen_prompt.json") as f:
    input = json.load(f)

with open("tests/acvp/keygen_expectedResults.json") as f:
    expectedResults = json.load(f)

expected = {}
# 1: {"tcId": 1, "ek": "1CAB...", "dk": "C8D4..."} in expected
for group in expectedResults["testGroups"]:
    for test in group["tests"]:
        expected[test["tcId"]] = test

def test_keygen():
    for group in input["testGroups"]:
        p = k_map[group["parameterSet"]]
        params.k    = p["k"]
        params.eta1 = p["eta1"]
        params.du   = p["du"]
        params.dv   = p["dv"]
        for test in group["tests"]:
            print(test["tcId"], group["parameterSet"])
            if test["tcId"] == 1 and group["parameterSet"] == "ML-KEM-512":
                print("\n" + "="*50)
                print(f"DEBUG für tcId=1 (ML-KEM-512)")
                print("="*50)
                
                z = bytes.fromhex(test["z"])
                d = bytes.fromhex(test["d"])
                
                # 1. G(d) testen
                rho, sigma = G(d)
                print(f"d: {d.hex()}")
                print(f"rho: {rho.hex()}")
                print(f"sigma: {sigma.hex()}")

                # Variante 1: G(d)
                rho, sigma = G(d)

                # Variante 2: G(d || k) 
                rho2, sigma2 = G(d + bytes([params.k]))  # für ML-KEM-512: k=2

                print(f"G(d)      rho: {rho.hex()}")
                print(f"G(d||k) rho: {rho2.hex()}")
                
                # 2. Ersten PRF-Aufruf für s[0] testen
                N = 0
                prf_s0 = PRF(params.eta1, sigma, N)
                print(f"PRF(s[0]): {prf_s0.hex()[:64]}...")
                
                # 3. s[0] aus CBD
                s0 = sample_poly_cbd(prf_s0, params.eta1)
                print(f"s[0][:10]: {s0.coeff[:10]}")
                
                # 4. NTT(s[0])
                s0_ntt = NTT(s0.coeff)
                print(f"NTT(s[0])[:10]: {s0_ntt[:10]}")
                
                # 5. Kompletten keygen durchlaufen
                ek, dk = kem._keygen_internal(d, z)
                print(f"MEIN ek[:32]: {ek[:32].hex()}")
                print(f"SOLL ek[:32]: {expected[test['tcId']]['ek'][:32]}")
                print(f"MEIN dk[:32]: {dk[:32].hex()}")
                print(f"SOLL dk[:32]: {expected[test['tcId']]['dk'][:32]}")
                
                # Weiter mit normalem Test
                assert ek == bytes.fromhex(expected[test["tcId"]]["ek"])
                assert dk == bytes.fromhex(expected[test["tcId"]]["dk"])
