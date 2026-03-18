from ntt import mul_NTT
import params

class poly:
    """Polynomial in Rq = Zq[x]/(x^n + 1)"""
    def __init__(self, coeff):
        self.coeff = coeff
        self.n = len(self.coeff)

    def __add__(self, poly_b):
        result = []
        for i in range(self.n):
            tmp = (self.coeff[i] + poly_b.coeff[i]) % params.q
            result.append(tmp)
        return poly(result)

    def __sub__(self, poly_b):
        result = []
        for i in range(self.n):
            tmp = (self.coeff[i] - poly_b.coeff[i]) % params.q
            result.append(tmp)
        return poly(result)

    def __mul__(self, poly_b):
        """takes only NTT as input!"""
        return poly(mul_NTT(self.coeff, poly_b.coeff))
         
    def poly_reduce(self):
        for i in range(len(self.coeff)):
            self.coeff[i] = self.coeff[i] % params.q