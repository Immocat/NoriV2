import numpy as np
import sys
import scipy.special as sp


def fseries_convolve(a, ka, b, kb):
    n = ka + kb - 1
    c = np.zeros(n)
    for i in range(n):
        sum = 0.0
        lim = int(min(kb, ka - i))
        for j in range(lim):
            sum += b[j] * a[i + j]
        start = int(max(0, i - ka + 1))
        stop = int(min(kb, i + ka))
        for j in range(start, stop):
            sum += b[j] * a[np.abs(i - j)]
        if i < kb:
            sum += b[i] * a[0]
        if i == 0:
            sum = 0.5 * (sum + a[0] * b[0])
        c[i] = 0.5 * sum
    return c


def mbessel_ratio(k, B):
    eps = sys.float_info.epsilon
    invTwoB = 2.0 / B
    i = k
    D = 1.0 / (invTwoB * i)
    i += 1.0
    Cd = D
    C = Cd

    while np.abs(Cd) > eps * np.abs(C):
        coeff = invTwoB * i
        i += 1.0
        D = 1.0 / (D + coeff)
        Cd *= coeff * D - 1.0
        C += Cd

    return C


def expcos_fseries(A, B, m):
    coeffs = np.zeros(m + 1)
    # /* Determine the last ratio and work downwards */
    coeffs[m] = mbessel_ratio(B, m)
    for i in range(m - 1, 0, -1):
        coeffs[i] = B / (2 * i + B * coeffs[i + 1])
        # /* Evaluate the exponentially scaled I0 and correct scaling */
    coeffs[0] = np.exp(A + B) * sp.i0e(B)
    # /* Apply the ratios & factor of two upwards */
    prod = 2 * coeffs[0]
    for i in range(1, m + 1):
        prod *= coeffs[i]
        coeffs[i] = prod

    return coeffs


def expcosCoefficientCount(B, relerr):
    prod = 1
    invB = 1.0 / B
    if B == 0:
        return 1
    i = 0
    while True:
        prod /= 1 + i * invB

        if prod < relerr:
            return i + 1
        i += 1