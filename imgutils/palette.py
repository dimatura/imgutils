from collections import OrderedDict
from PIL import Image
import numpy as np


__all__ = ['add_color_palette']


def add_color_palette(img, class_id_to_rgb):
    """ Add color palette to 8-bit PIL image.

    :parameters:
        - `class_id_to_rgb`: dict or list.
        Colors must be integers in (0, 255) range.
    """
    if not isinstance(img, Image.Image):
        img = Image.fromarray(img)
        if img.mode == 'RGB':
            raise ValueError('Invalid image mode (RGB)')

    if (isinstance(class_id_to_rgb, dict) or
        isinstance(class_id_to_rgb, OrderedDict)):
        class_id_to_rgb_lst = []
        keys = sorted(class_id_to_rgb.keys())
        max_key = np.max(keys)
        for k in xrange(max_key+1):
            rgb = class_id_to_rgb.get(k, (0, 0, 0))
            class_id_to_rgb_lst.append(rgb)
    else:
        class_id_to_rgb_lst = class_id_to_rgb

    class_id_to_rgb_lst_flat = []
    for rgb in class_id_to_rgb_lst:
        class_id_to_rgb_lst_flat.extend(list(rgb))

    img.putpalette(class_id_to_rgb_lst_flat)
    return img
