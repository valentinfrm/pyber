import timeit

from kyber_py.ml_kem import ML_KEM_512, ML_KEM_768, ML_KEM_1024

from pyber import params
from pyber.kem import keygen, encaps, decaps

k_map = {
    "ML-KEM-512":  {"k": 2, "eta1": 3, "du": 10, "dv": 4},
    "ML-KEM-768":  {"k": 3, "eta1": 2, "du": 10, "dv": 4},
    "ML-KEM-1024": {"k": 4, "eta1": 2, "du": 11, "dv": 5},
}

def to_ms(time):
    return time / 100 * 1000

def set_params(version):
    for key, value in k_map[version].items():
        setattr(params, key, value) # sets params.key = value

result = {
    "pyber": {} ,
    "kyber_py": {}
}

# ===== 512 =====
set_params("ML-KEM-512")
ek, dk = keygen()
K, c = encaps(ek)

result["pyber"]["512-keygen"] = to_ms(min(timeit.repeat('keygen()', number=25, globals=globals())))
result["pyber"]["512-encaps"] = to_ms(min(timeit.repeat('encaps(ek)', number=25, globals=globals())))
result["pyber"]["512-decaps"] = to_ms(min(timeit.repeat('decaps(dk, c)', number=25, globals=globals())))

ek, dk = ML_KEM_512.keygen()
K, c = ML_KEM_512.encaps(ek)

result["kyber_py"]["512-keygen"] = to_ms(min(timeit.repeat('ML_KEM_512.keygen()', number=25, globals=globals())))
result["kyber_py"]["512-encaps"] = to_ms(min(timeit.repeat('ML_KEM_512.encaps(ek)', number=25, globals=globals())))
result["kyber_py"]["512-decaps"] = to_ms(min(timeit.repeat('ML_KEM_512.decaps(dk, c)', number=25, globals=globals())))

# ===== 768 =====
set_params("ML-KEM-768")
ek, dk = keygen()
K, c = encaps(ek)

result["pyber"]["768-keygen"] = to_ms(min(timeit.repeat('keygen()', number=25, globals=globals())))
result["pyber"]["768-encaps"] = to_ms(min(timeit.repeat('encaps(ek)', number=25, globals=globals())))
result["pyber"]["768-decaps"] = to_ms(min(timeit.repeat('decaps(dk, c)', number=25, globals=globals())))

ek, dk = ML_KEM_768.keygen()
K, c = ML_KEM_768.encaps(ek)

result["kyber_py"]["768-keygen"] = to_ms(min(timeit.repeat('ML_KEM_768.keygen()', number=25, globals=globals())))
result["kyber_py"]["768-encaps"] = to_ms(min(timeit.repeat('ML_KEM_768.encaps(ek)', number=25, globals=globals())))
result["kyber_py"]["768-decaps"] = to_ms(min(timeit.repeat('ML_KEM_768.decaps(dk, c)', number=25, globals=globals())))

# ===== 1024 =====
set_params("ML-KEM-1024")
ek, dk = keygen()
K, c = encaps(ek)

result["pyber"]["1024-keygen"] = to_ms(min(timeit.repeat('keygen()', number=25, globals=globals())))
result["pyber"]["1024-encaps"] = to_ms(min(timeit.repeat('encaps(ek)', number=25, globals=globals())))
result["pyber"]["1024-decaps"] = to_ms(min(timeit.repeat('decaps(dk, c)', number=25, globals=globals())))

ek, dk = ML_KEM_1024.keygen()
K, c = ML_KEM_1024.encaps(ek)

result["kyber_py"]["1024-keygen"] = to_ms(min(timeit.repeat('ML_KEM_1024.keygen()', number=25, globals=globals())))
result["kyber_py"]["1024-encaps"] = to_ms(min(timeit.repeat('ML_KEM_1024.encaps(ek)', number=25, globals=globals())))
result["kyber_py"]["1024-decaps"] = to_ms(min(timeit.repeat('ML_KEM_1024.decaps(dk, c)', number=25, globals=globals())))

for imp, values in result.items():
    print(f"=== {imp} ====")
    for key, value in values.items():
        print(f"{key}: {value}")