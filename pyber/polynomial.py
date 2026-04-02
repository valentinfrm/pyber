from pyber.ntt import mul_NTT
from pyber import params

class poly:
    """Polynomial in Rq = Zq[x]/(x^n + 1)"""
    def __init__(self, coeff):
        self.coeff = coeff
        self.n = len(self.coeff)

    def __add__(self, poly_b):
        if self.n != len(poly_b.coeff):
            raise ValueError("Only polynomials of the same degree can be added")
        
        result = [0] * self.n
        for i in range(self.n):
            result[i] = (self.coeff[i] + poly_b.coeff[i]) % params.q
        return poly(result)

    def __sub__(self, poly_b):
        if self.n != len(poly_b.coeff):
            raise ValueError("Only polynomials of the same degree can be subtracted")
        
        result = [0] * self.n
        for i in range(self.n):
            result[i] = (self.coeff[i] - poly_b.coeff[i]) % params.q
        return poly(result)

    def __mul__(self, poly_b):
        """takes only NTT as input!"""
        return poly(mul_NTT(self.coeff, poly_b.coeff))
         
    def poly_reduce(self):
        for i in range(len(self.coeff)):
            self.coeff[i] = self.coeff[i] % params.q