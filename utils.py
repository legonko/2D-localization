import numpy as np


def convolve(a, b):
    out_shape = np.array((a.shape, b.shape)).max(0)
    fa = np.fft.fftn(a, out_shape)
    fb = np.fft.fftn(b, out_shape)
    out = np.fft.ifftn(fa * fb).real
    out[abs(out) < out.mean() * 1e-13] = 0.0

    return out