from field import *

class poly:
    """Polynomial in Rq = Zq[x]/(x^n + 1)"""
    def __init__(self, coeff):
        self.coeff = coeff
        self.n = len(self.coeff)

    def __add__(self, poly_b):
        result = []
        for i in range(self.n):
            tmp = add(self.coeff[i], poly_b.coeff[i])
            result.append(tmp)
        return poly(result)

    def __sub__(self, poly_b):
        result = []
        for i in range(self.n):
            tmp = sub(self.coeff[i], poly_b.coeff[i])
            result.append(tmp)
        return poly(result)

    def __mul__(self, poly_b):
        """multiply using negacyclic convolution -> NTT later"""
        result = []
        tmp = list(self.coeff) # copy coeffs to avoid overwriting while reading
        for row in range(self.n):
            c = 0
            for col in range(self.n): 
                og_index = (row - col) % self.n # index in original poly (wraps around negacyclically)
                v = mul(tmp[og_index], poly_b.coeff[col])
                if col > row:
                    v = -v # negate when index wrapped around (x^n = -1)
                c += v
            result.append(reduce(c))
        return poly(result)
            
    def poly_reduce(self):
        for i in range(len(self.coeff)):
            self.coeff[i] = reduce(self.coeff[i])