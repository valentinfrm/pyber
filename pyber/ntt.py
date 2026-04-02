from pyber import params

# TODO: fully grasp concepts

# zeta^BitRev7(i) mod q for i in 0...127
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

# zeta^(2*BitRev7(i)+1) mod q for i in 0...127
ZETAS_MUL = [17, -17, 2761, -2761, 583, -583, 2649, -2649,
             1637, -1637, 723, -723, 2288, -2288, 1100, -1100,
             1409, -1409, 2662, -2662, 3281, -3281, 233, -233,
             756, -756, 2156, -2156, 3015, -3015, 3050, -3050,
             1703, -1703, 1651, -1651, 2789, -2789, 1789, -1789,
             1847, -1847, 952, -952, 1461, -1461, 2687, -2687,
             939, -939, 2308, -2308, 2437, -2437, 2388, -2388,
             733, -733, 2337, -2337, 268, -268, 641, -641,
             1584, -1584, 2298, -2298, 2037, -2037, 3220, -3220,
             375, -375, 2549, -2549, 2090, -2090, 1645, -1645,
             1063, -1063, 319, -319, 2773, -2773, 757, -757,
             2099, -2099, 561, -561, 2466, -2466, 2594, -2594,
             2804, -2804, 1092, -1092, 403, -403, 1026, -1026,
             1143, -1143, 2150, -2150, 2775, -2775, 886, -886,
             1722, -1722, 1212, -1212, 1874, -1874, 1029, -1029,
             2110, -2110, 2935, -2935, 885, -885, 2154, -2154]

def NTT(f):
    """
    transforms a polynomial from R_q to T_q using NTT

    Args:
        f (list): 256 coeffs in Z_q

    Returns:
        list: 256 coeffs in NTT (T_q)
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
    """
    transforms a polynomial from T_q back to R_q using inverse NTT

    Args:
        f (list): 256 coeffs in NTT (T_q)

    Returns:
        list: 256 coeffs in Z_q
    """
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

def mul_NTT(f, g):
    """
        multiplies two NTT polynomials in T_q (NTT realm)

        Args:
            f (list): coeffs of a polynomial in NTT
            g (list): coeffs of a polynomial in NTT

        Returns:
            h (list): coeffs of product in NTT
    """
    h = [0] * 256
    for i in range(128):
        h[2 * i], h[2 * i + 1] = mul_base_case(
            f[2 * i], f[2 * i + 1],
            g[2 * i], g[2 * i + 1],
            ZETAS_MUL[i]
        )
    return h
        



def mul_base_case(a0, a1, b0, b1, gamma):
    """
        multiplies two linear polynomes in mod (x^2 - gamma)

        Args:
            a0 (int): a0 * a1x
            a1 (int): a0 * a1x
            b0 (int): b0 * b1x
            b1 (int): b0 * b1x
            gamma (int): zeta^(2*BitRev7(i)+1)
        
        Returns:
            tuple: (c0, c1) c0 * c1x
    """
    c0 = (a0 * b0 + a1 * b1 * gamma) % params.q # x^2 - gamma = 0 => x^2 = gamma
    c1 = (a0 * b1 + a1 * b0) % params.q
    return c0, c1
