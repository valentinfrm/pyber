import json
import kem
import params

k_map = {
    "ML-KEM-512":  {"k": 2, "eta1": 3, "du": 10, "dv": 4},
    "ML-KEM-768":  {"k": 3, "eta1": 2, "du": 10, "dv": 4},
    "ML-KEM-1024": {"k": 4, "eta1": 2, "du": 11, "dv": 5},
}

with open("pytest/caps_prompt.json") as f:
    input = json.load(f)

with open("pytest/caps_expectedResults.json") as f:
    expected_results = json.load(f)

expected = {}
for group in expected_results["testGroups"]:
    for test in group["tests"]:
        expected[test["tcId"]] = test

def _run_check(function, *args):
    try:
        function(*args)
        return True
    except(TypeError, ValueError):
        return False

def test_capsulation():
    for group in input["testGroups"]:
        function = group["function"]
        p = k_map[group["parameterSet"]]
        params.k    = p["k"]
        params.eta1 = p["eta1"]
        params.du   = p["du"]
        params.dv   = p["dv"]
        for test in group["tests"]:
            if function == "encapsulation":
                ek = bytes.fromhex(test["ek"])
                m = bytes.fromhex(test["m"])
                K, c = kem._encaps_internal(ek, m)
                assert K == bytes.fromhex(expected[test["tcId"]]["k"])
                assert c == bytes.fromhex(expected[test["tcId"]]["c"])

            elif function == "decapsulation":
                dk = bytes.fromhex(test["dk"])
                c = bytes.fromhex(test["c"])
                K = kem._decaps_internal(dk, c)
                assert K == bytes.fromhex(expected[test["tcId"]]["k"])

            elif function == "decapsulationKeyCheck":
                dk = bytes.fromhex(test["dk"])
                result = _run_check(kem._dk_check, dk)
                assert result == expected[test["tcId"]]["testPassed"] 

            elif function == "encapsulationKeyCheck":
                ek = bytes.fromhex(test["ek"])
                result = _run_check(kem.encaps_check, ek)
                assert result == expected[test["tcId"]]["testPassed"] 

            
