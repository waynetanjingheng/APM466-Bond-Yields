from math import pow, log

# Credit goes to `jsogarro` on GitHub for the helper functions to calculate the tvm https://github.com/jsogarro/mortgage_analytics/blob/master/tvm.py


def newton(f, fArg, x0, y, maxIter, minError):
    """_summary_

    Args:
        f (func): function returning a float
        x0 (float: initial value
        y (float): desired value
        maxIter (int): maximum number of iterations allowed
        minError (float): minimum error abs(f(x)-y)
    """

    def func(f, fArg, x, y):
        return f(x, fArg) - y

    def slope(f, fArg, x, y):
        xp = x * 1.05
        return (func(f, fArg, xp, y) - func(f, fArg, x, y)) / (xp - x)

    counter = 0
    while 1:
        sl = slope(f, fArg, x0, y)
        x0 = x0 - func(f, fArg, x0, y) / sl
        if counter > maxIter:
            break
        if abs(f(x0, fArg) - y) < minError:
            break
        counter += 1
    return x0


class TVM:
    bgn, end = 0, 1

    def __str__(self):
        return "n=%f, r=%f, pv=%f, pmt=%f, fv=%f" % (
            self.n,
            self.r,
            self.pv,
            self.pmt,
            self.fv,
        )

    def __init__(self, n=0.0, r=0.0, pv=0.0, pmt=0.0, fv=0.0, mode=end):
        self.n = float(n)
        self.r = float(r)
        self.pv = float(pv)
        self.pmt = float(pmt)
        self.fv = float(fv)
        self.mode = mode

    def calc_pv(self):
        z = pow(1 + self.r, -self.n)
        pva = self.pmt / self.r
        if self.mode == TVM.bgn:
            pva += self.pmt
        return -(self.fv * z + (1 - z) * pva)

    def calc_fv(self):
        z = pow(1 + self.r, -self.n)
        pva = self.pmt / self.r
        if self.mode == TVM.bgn:
            pva += self.pmt
        return -(self.pv + (1 - z) * pva) / z

    def calc_pmt(self):
        z = pow(1 + self.r, -self.n)
        if self.mode == TVM.bgn:
            return (self.pv + self.fv * z) * self.r / (z - 1) / (1 + self.r)
        else:
            return (self.pv + self.fv * z) * self.r / (z - 1)

    def calc_n(self):
        pva = self.pmt / self.r
        if self.mode == TVM.bgn:
            pva += self.pmt
        z = (-pva - self.pv) / (self.fv - pva)
        return -log(z) / log(1 + self.r)

    def calc_r(self):
        def function_fv(r, self):
            z = pow(1 + r, -self.n)
            pva = self.pmt / r
            if self.mode == TVM.bgn:
                pva += self.pmt
            return -(self.pv + (1 - z) * pva) / z

        return newton(
            f=function_fv, fArg=self, x0=0.05, y=self.fv, maxIter=1000, minError=0.0001
        )
