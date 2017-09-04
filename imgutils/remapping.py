from collections import OrderedDict
from PIL import Image
import numpy as np


__all__ = ['rgb_image_to_label_image',
           'label_image_to_rgb_image',
           'remap_labels']


def rgb_image_to_label_image(img, mapping, default=0):
    """ Map RGB image to label image.

    :parameters:
        - img: HxWx3 uint8 image (numpy array)
        - mapping: dictionary of (r,g,b) -> int
        - default: label to use for keys not in mapping
    """
    if img.ndim != 3:
        raise ValueError('img must be HxWx3 matrix')
    if img.shape[2] != 3:
        raise ValueError('img must be HxWx3 matrix')

    img2 = img.astype('uint32')

    # assign a unique integer to each (r, g, b) tuple
    rshift = img2[:,:,0]<<16
    gshift = img2[:,:,1]<<8
    bshift = img2[:,:,2]
    imgh = np.bitwise_or(np.bitwise_or(rshift, gshift), bshift)

    # create a big table with one entry for each 256**3-1 colors
    # 16777216 == 255*(2**16) + 255*(2**8) + 255 + 1 == 256**3
    rgb_tab = np.zeros(16777216, dtype='uint32')
    if default != 0:
        rgb_tab.fill(default)

    # fill table with labels in mapping
    for k, v in mapping.iteritems():
        hk = k[0]*(2**16) + k[1]*(2**8) + k[2]
        rgb_tab[hk] = v

    # take() is slightly faster
    # limg2 = rgb_tab[imgh]
    limg2 = np.take(rgb_tab, imgh)
    return limg2


def label_image_to_rgb_image(label_img, mapping, default=[255, 255, 255]):
    """ Map integer label image to rgb image.

    :parameters:
        - label_img: int image
        - mapping: dictionary of int -> (r, g, b)
        - default: default rgb
    """
    lbl_max = np.max(mapping.keys())
    label_tab = np.empty((lbl_max+1, 3), dtype='u1')
    label_tab[:] = default
    for lbl_src, lbl_dst in mapping.iteritems():
        label_tab[lbl_src] = lbl_dst
    return label_tab[label_img]


def remap_labels(label_img, mapping, default=-1):
    """ Map integer labels to integer labels.

    :parameters:
        - label_img: int image
        - mapping: dictionary of int -> int
        - default: default int
    """
    lbl_max = np.max(mapping.keys())
    label_tab = np.empty((lbl_max+1), dtype='int64')
    label_tab.fill(default)
    for lbl_src, lbl_dst in mapping.iteritems():
        label_tab[lbl_src] = lbl_dst
    return label_tab[label_img]


if __name__ == '__main__':
    import doctest
    flags = doctest.REPORT_NDIFF
    fail, total = doctest.testmod(optionflags=flags)
    print("{} failures out of {} tests".format(fail, total))

