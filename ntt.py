import params

ZETAS = [1, 1729, 2580, 3289, 2642, 630, 1897, 848,
         1062, 1919, 193, 797, 2786, 3260, 569, 1746,
         296, 2447, 1339, 1476, 3046, 56, 2240, 1333,
         1426, 2094, 535, 2882, 2393, 2879, 1974, 821,
         289, 331, 3253, 1756, 1197, 2304, 2277, 2055,
         650, 1977, 2513, 632, 2865, 33, 1320, 1915,
         2319, 1435, 807, 452, 1438, 2868, 1534, 2402,
         2647, 2617, 1481, 648, 2474, 3110, 1227, 910,
         17, 2761, 583, 2649, 1637, 723, 2288, 1100,
         1409, 2662, 3281, 233, 756, 2156, 3015, 3050,
         1703, 1651, 2789, 1789, 1847, 952, 1461, 2687,
         939, 2308, 2437, 2388, 733, 2337, 268, 641,
         1584, 2298, 2037, 3220, 375, 2549, 2090, 1645,
         1063, 319, 2773, 757, 2099, 561, 2466, 2594,
         2804, 1092, 403, 1026, 1143, 2150, 2775, 886,
         1722, 1212, 1874, 1029, 2110, 2935, 885, 2154]

def NTT(f):
    """
        FFT but zeta instead of omega
        TODO: understand fully
    """
    f = list(f)  # copy
    k = 1
    length = params.n // 2 # split list in i and i + length

    while length >= 2: # no 512th root of unity in Z_q
        for start in range(0, 256, 2 * length): # 2 * length = block size
            zeta = ZETAS[k]
            k += 1
            for j in range(start, start + length):
                t = zeta * f[j + length] % params.q
                f[j + length] = (f[j] - t) % params.q
                f[j]          = (f[j] + t) % params.q
        length //= 2
    
    return f

def iNTT(f):
    """ inverse NTT """
    f = list(f)
    k = 127
    length = 2
    
    while length <= 128:
        for start in range(0, 256, 2 * length):
            zeta = ZETAS[k]
            k -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j]          = (t + f[j + length]) % params.q
                f[j + length] = (zeta * (f[j + length] - t)) % params.q
        length *= 2
    
    f = [x * 3303 % params.q for x in f]
    
    return f
