import numpy as np


def convolve(a, b):
    out_shape = np.array((a.shape, b.shape)).max(0)
    fa = np.fft.fftn(a, out_shape)
    fb = np.fft.fftn(b, out_shape)
    out = np.fft.ifftn(fa * fb).real
    out[abs(out) < out.mean() * 1e-13] = 0.0

    return out

def print_matrix(m, lbl):
    p = 0
    rows, columns = np.shape(m)
    m = m[2:(rows - 2), 2:(columns - 2)]
    for i in range(len(m)):
        res = ('  '.join(['{:.2f}'.format(x) for x in m[i]]))
        p += 20
        lbl.create_label(res, 554, 84 + p, (61, 61, 61))

def print_vector(v, lbl):
    p = 0
    for i in v:
        res = ('  '.join(['{:.2f}'.format(i)]))
        p += 32
        lbl.create_label(res, 774 + p, 36, (61, 61, 61))