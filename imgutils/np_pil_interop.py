import numpy as np
from PIL import Image

def wrapargs_pil_fn(fn, *args, **kwargs):
    args2 = []
    for arg in args:
        if np.isinstance(arg, np.array):
            try:
                args2.append(Image.fromarray(arg))
            except TypeError:
                args2.apppend(arg)
    return fn(*args2, **kwargs)
