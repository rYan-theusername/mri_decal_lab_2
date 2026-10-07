import numpy as np

def bruce(t):
    """ Parameterizes the Batman curve for 0 < t < 1 from https://mathworld.wolfram.com/BatmanCurve.html """
    x = np.zeros_like(t)
    y = np.zeros_like(t)

    upper_mask = t <= 0.5       # [0, 0.5] parameterizes upper half
    lower_mask = ~upper_mask    # [0, 1.0] parameterizes lower half

    # goes -7 -> +7 -> -7
    x[upper_mask] = -7.0 + 28.0 * t[upper_mask]
    x[lower_mask] = 7.0 - 28.0 * (t[lower_mask] - 0.5)

    def H(v):   # heaviside step function
        return np.where(v >= 0, 1.0, 0.0)

    def safe_sqrt(v): # for handling sqrt(negative)
        return np.sqrt(np.maximum(0.0, v))

    # building blocks eqs 3, 4, 5, 6
    w = 3.0 * safe_sqrt(1.0 - (x / 7.0)**2)
    l = 0.5 * (x + 3.0) - (3.0 / 7.0) * safe_sqrt(10.0) * safe_sqrt(4.0 - (x + 1.0)**2) + (6.0 / 7.0) * safe_sqrt(10.0)
    r = 0.5 * (3.0 - x) - (3.0 / 7.0) * safe_sqrt(10.0) * safe_sqrt(4.0 - (x - 1.0)**2) + (6.0 / 7.0) * safe_sqrt(10.0)
    h = 0.5 * (3.0 * (np.abs(x + 0.5) + np.abs(x - 0.5) + 6.0) - 11.0 * (np.abs(x + 0.75) + np.abs(x - 0.75)))

    # upper curve eq 1
    f_x = (h - l) * H(x + 1.0) + (r - h) * H(x - 1.0) + (l - w) * H(x + 3.0) + (w - r) * H(x - 3.0) + w

    # lower curve eq 2
    g_inner = (np.abs(0.5 * x)
               + safe_sqrt(1.0 - (np.abs(np.abs(x) - 2.0) - 1.0)**2)
               - (1.0 / 112.0) * (3.0 * safe_sqrt(33.0) - 7.0) * (x**2)
               + 3.0 * safe_sqrt(1.0 - (x / 7.0)**2) - 3.0)

    g_x = 0.5 * g_inner * (np.sign(x + 4.0) - np.sign(x - 4.0)) - 3.0 * safe_sqrt(1.0 - (x / 7.0)**2)

    y[upper_mask] = f_x[upper_mask]
    y[lower_mask] = g_x[lower_mask]

    return x, y
