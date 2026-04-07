import timeit

from kyber_py.ml_kem import ML_KEM_512, ML_KEM_768, ML_KEM_1024
import matplotlib.pyplot as plt
import numpy as np

from pyber import params
from pyber.kem import keygen, encaps, decaps

RUN_AMOUNT = 1

GREEN_LIGHT = "#E5FF54"
GREEN_DARK = "#1C812A"

BLUE_LIGHT = "#BBD0FE"
BLUE_DARK = "#3B83FF"

RED_LIGHT = "#fd6969"
RED_DARK = "#f51827"

k_map = {
    "ML-KEM-512":  {"k": 2, "eta1": 3, "du": 10, "dv": 4},
    "ML-KEM-768":  {"k": 3, "eta1": 2, "du": 10, "dv": 4},
    "ML-KEM-1024": {"k": 4, "eta1": 2, "du": 11, "dv": 5},
}

def to_ms(time):
    return round(time / RUN_AMOUNT * 1000, 2) # round to 2 decimal points

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

# globals make module-level names available to timeit
result["pyber"]["512-keygen"] = to_ms(min(timeit.repeat('keygen()', number=RUN_AMOUNT, globals=globals())))
result["pyber"]["512-encaps"] = to_ms(min(timeit.repeat('encaps(ek)', number=RUN_AMOUNT, globals=globals())))
result["pyber"]["512-decaps"] = to_ms(min(timeit.repeat('decaps(dk, c)', number=RUN_AMOUNT, globals=globals())))

ek, dk = ML_KEM_512.keygen()
K, c = ML_KEM_512.encaps(ek)

result["kyber_py"]["512-keygen"] = to_ms(min(timeit.repeat('ML_KEM_512.keygen()', number=RUN_AMOUNT, globals=globals())))
result["kyber_py"]["512-encaps"] = to_ms(min(timeit.repeat('ML_KEM_512.encaps(ek)', number=RUN_AMOUNT, globals=globals())))
result["kyber_py"]["512-decaps"] = to_ms(min(timeit.repeat('ML_KEM_512.decaps(dk, c)', number=RUN_AMOUNT, globals=globals())))

# ===== 768 =====
set_params("ML-KEM-768")
ek, dk = keygen()
K, c = encaps(ek)

result["pyber"]["768-keygen"] = to_ms(min(timeit.repeat('keygen()', number=RUN_AMOUNT, globals=globals())))
result["pyber"]["768-encaps"] = to_ms(min(timeit.repeat('encaps(ek)', number=RUN_AMOUNT, globals=globals())))
result["pyber"]["768-decaps"] = to_ms(min(timeit.repeat('decaps(dk, c)', number=RUN_AMOUNT, globals=globals())))

ek, dk = ML_KEM_768.keygen()
K, c = ML_KEM_768.encaps(ek)

result["kyber_py"]["768-keygen"] = to_ms(min(timeit.repeat('ML_KEM_768.keygen()', number=RUN_AMOUNT, globals=globals())))
result["kyber_py"]["768-encaps"] = to_ms(min(timeit.repeat('ML_KEM_768.encaps(ek)', number=RUN_AMOUNT, globals=globals())))
result["kyber_py"]["768-decaps"] = to_ms(min(timeit.repeat('ML_KEM_768.decaps(dk, c)', number=RUN_AMOUNT, globals=globals())))

# ===== 1024 =====
set_params("ML-KEM-1024")
ek, dk = keygen()
K, c = encaps(ek)

result["pyber"]["1024-keygen"] = to_ms(min(timeit.repeat('keygen()', number=RUN_AMOUNT, globals=globals())))
result["pyber"]["1024-encaps"] = to_ms(min(timeit.repeat('encaps(ek)', number=RUN_AMOUNT, globals=globals())))
result["pyber"]["1024-decaps"] = to_ms(min(timeit.repeat('decaps(dk, c)', number=RUN_AMOUNT, globals=globals())))

ek, dk = ML_KEM_1024.keygen()
K, c = ML_KEM_1024.encaps(ek)

result["kyber_py"]["1024-keygen"] = to_ms(min(timeit.repeat('ML_KEM_1024.keygen()', number=RUN_AMOUNT, globals=globals())))
result["kyber_py"]["1024-encaps"] = to_ms(min(timeit.repeat('ML_KEM_1024.encaps(ek)', number=RUN_AMOUNT, globals=globals())))
result["kyber_py"]["1024-decaps"] = to_ms(min(timeit.repeat('ML_KEM_1024.decaps(dk, c)', number=RUN_AMOUNT, globals=globals())))

def print_result():
    for imp, values in result.items():
        print(f"=== {imp} ====")
        for key, value in values.items():
            print(f"{key}: {value}")

# ===== plotting =====
def get_data(op):
    sizes = ["512", "768", "1024"]

    pyber_data = [result["pyber"][f"{s}-{op}"] for s in sizes]
    kyber_py_data = [result["kyber_py"][f"{s}-{op}"] for s in sizes]

    return pyber_data, kyber_py_data

def plot(op, ax):
    versions = ["512 Bit", "768 Bit", "1024 Bit"]
    x = np.arange(len(versions)) # creates [0, 1, 2 ...]
    pyber_data, kyber_py_data = get_data(op)
    w = 0.275 # bar width

    bar_1 = ax.bar(x-w/2, width=w, height=pyber_data, label="Pyber", color=BLUE_LIGHT)
    bar_2 = ax.bar(x+w/2, width=w, height=kyber_py_data, label="Kyber-py", color=BLUE_DARK)

    ax.bar_label(bar_1)
    ax.bar_label(bar_2)
    ax.set_xticks(x)
    ax.set_xticklabels(versions)
    ax.set_title(f"{op}()", fontsize=14)
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))  # large steps
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.25)) # small steps
    ax.yaxis.grid(True, alpha=0.2)
    ax.set_axisbelow(True) # moves yaxis grid behind bars

plt.style.use('dark_background')
plt.rcParams['font.family'] = 'monospace'
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(16, 9))

plt.subplots_adjust(
    left=0.075, 
    right=0.925, 
    bottom=0.1, 
    top=0.9
    ) # x: plot[left -> right]

plot("keygen", ax1)
plot("encaps", ax2)
plot("decaps", ax3)

ax1.legend(loc='upper left')
ax1.set_ylabel("ms", fontsize=14, labelpad=15)

plt.subplots_adjust(left=0.075, right=0.925, bottom=0.1, top=0.9) # x: plot[left -> right]
plt.savefig("assets/benchmark.png", dpi=200)
# plt.show()