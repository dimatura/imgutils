from __future__ import print_function


__all__ = ['smart_resize',
           'letterbox_resize',
           'trim_percentage',
           'crop_center',
           'add_border',
           'draw_bbox',
           'hstack',
           'vstack',
           'dstack_rgb',
           'square_montage',
           'montage']



import math

import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


def _default_color(mode, c, transparent=False):
    if mode == 'L':
        color = c
    elif mode == 'RGB':
        color = (c, c, c)
    elif mode == 'RGBA':
        color = (c, c, c, 0 if transparent else 255)
    return color


def _all_equal(seq):
    for x in seq:
        if x != seq[0]:
            return False
    return True


def letterbox_resize(img, img_wh, bg=None, interp=None):
    """
    Use PIL thumbnail to resize. May letterbox output in
    order to keep aspect ratio.

    :parameters:
        - img: input Image
        - img_wh: desired width, height
        - bg: int or tuple(int, int, int) or tuple(int, int, int, int)
            color for background as rgb int tuple
        - interp: int
            interpolation code from PIL.Image

    >>> img = Image.new('L', (128, 128))
    >>> imgr = letterbox_resize(img, (20, 20))
    >>> imgr.size
    (20, 20)
    >>> imgr2 = letterbox_resize(img, (40, 20))
    >>> imgr2.size
    (40, 20)
    >>> imgr3 = letterbox_resize(img, (200, 200))
    >>> imgr3.size
    (200, 200)
    """

    w, h = img_wh
    if bg is None:
        bg = _default_color(img.mode, 0, transparent=False)

    if interp is None:
        if img.size[0] >= w or img.size[1] >= h:
            interp = Image.ANTIALIAS
        else:
            interp = Image.BICUBIC

    img = img.copy()
    img.thumbnail((w, h), interp)
    newimg = Image.new(img.mode, (w, h), bg)
    left = int(math.floor((newimg.size[0]-img.size[0])*.5))
    top = int(math.floor((newimg.size[1]-img.size[1])*.5))
    newimg.paste(img, (left, top))
    return newimg


def smart_resize(img, img_wh, interp=None):
    """
    adjusts either w or h, depending on which is None (or <= 0)

    :parameters:
        - img: input Image
        - img_wh: desired width, height
        - interp: int
            interpolation code from PIL.Image

    >>> img = Image.new('L', (128, 128))
    >>> imgr = smart_resize(img, (None, 256))
    >>> imgr.size
    (256, 256)
    >>> imgr2 = smart_resize(img, (256, None))
    >>> imgr2.size
    (256, 256)
    >>> imgr3 = smart_resize(img, (512, None))
    >>> imgr3.size
    (512, 512)
    """

    w, h = img_wh
    is_valid = lambda x: (x is not None) and (x > 0)
    if not is_valid(w) and not is_valid(h):
        raise ValueError("One of width or height must be specified")

    old_w, old_h = img.size
    ratio = float(old_w)/old_h
    if not is_valid(h):
        h = int(w/ratio)
    elif not is_valid(w):
        w = int(h*ratio)

    if interp is None:
        if old_w >= w or old_h >= h:
            interp = Image.ANTIALIAS
        else:
            interp = Image.BICUBIC

    img = img.resize((w, h), interp)
    return img



def trim_percentage(img, percentage):
    """
    trim percentage off images

    :parameters:
        - percentage: int
            percentage of dimension to trim off.
            both sides are trimmed, half each side.

    >>> img = Image.new('L', (100, 200))
    >>> imgt = trim_percentage(img, 10)
    >>> imgt.size
    (90, 180)
    """
    px_w = img.size[0]*(percentage/100.)
    px_h = img.size[1]*(percentage/100.)
    box = map(int, (px_w/2, px_h/2, img.size[0]-px_w/2, img.size[1]-px_h/2))
    img = img.crop(box)
    return img


def crop_center(img, img_wh):
    """
    crop box of size img_wh from center of image.
    assumes box is smaller than image.

    >>> img = Image.new('L', (128, 128))
    >>> imgc = crop_center(img, (50, 50))
    >>> imgc.size
    (50, 50)
    """
    w, h = img_wh
    if w > img.size[0] or h > img.size[1]:
        raise ValueError('crop dimensions larger than image')
    # box is left, upper, right, lower pixel
    # img.size is width, height
    size = (w, h)
    col0 = (img.size[0]-size[0])//2
    row0 = (img.size[1]-size[1])//2
    box = (col0, row0, col0+size[0], row0+size[1])
    return img.crop(box)


# def draw_tiny_text(img, text, pos, color):
#     """
#     draws tiny text on image.
#
#     :parameters:
#         - pos: tuple (int, int)
#             x, y position of text from top left (TODO)
#         - color: tuple (int, int, int)
#             rgb int tuple of text
#     """
#     # TODO hack! and cache the font
#     fontpath = (Path(__file__).realpath().parent)/'fonts/tom-thumb.pil'
#     assert( fontpath.exists() )
#     font = ImageFont.load(fontpath)
#     #font = ImageFont.load('fonts/tom-thumb.pil')
#     draw = ImageDraw.Draw(img)
#     draw.text(pos, text, font=font, fill=color)


def draw_bbox(img, bb, color=None):
    """ draw bounding on image in-place.
     :parameters:
        - bb: Sequence of either [(x0, y0), (x1, y1)] or [x0, y0, x1, y1]

    >>> img = Image.new('L', (128, 128))
    >>> draw_bbox(img, ((50, 50), (50+20, 50+20)))
    >>> rgbimg = Image.new('RGB', (128, 128))
    >>> draw_bbox(img, ((50, 50), (50+20, 50+20)))
    >>> rgbaimg = Image.new('RGBA', (128, 128))
    >>> draw_bbox(img, ((50, 50), (50+20, 50+20)))
    """
    if color is None:
        if img.mode == 'L':
            color = 255
        elif img.mode == 'RGB':
            color = (255, 0, 0)
        elif img.mode == 'RGBA':
            color = (255, 0, 0, 255)
    draw = ImageDraw.Draw(img)
    draw.rectangle(bb, fill=None, outline=color)


def add_border(img, px, color=None):
    """ add border to image.
    :parameters:
        - img: input Image
        - px: width in pixels
        - color: PIL color

    >>> img = Image.new('L', (128, 128))
    >>> imgb = add_border(img, 2)
    >>> imgb.size
    (132, 132)
    """

    if color is None:
        color = _default_color(img.mode, 0, transparent=False)
    return ImageOps.expand(img, px, color)


def hstack(images, variable_width=True):
    """ stack PIL images downwards.
    unless variable_width is False, width equals max width of all images.

    >>> img1 = Image.new('L', (128, 128))
    >>> img2 = Image.new('L', (128, 128))
    >>> imgs = hstack((img1, img2))
    >>> imgs.size
    (128, 256)
    >>> img3 = Image.new('L', (256, 128))
    >>> imgs2 = hstack((img1, img3))
    >>> imgs2.size
    (256, 256)
    """

    widths, heights = zip(*[img.size for img in images])

    if not variable_width and not _all_equal(widths):
        raise ValueError('widths must be the same')

    out_w = max(widths)
    out_h = sum(heights)
    out = Image.new(images[0].mode, (out_w, out_h))
    cum_h = 0
    for h, img in zip(heights, images):
        out.paste(img, (0, cum_h))
        cum_h += h
    return out


def vstack(images, variable_height=True):
    """ stack PIL images sideways.
    unless variable_height is False, height equals max height of all images.
    """

    widths, heights = zip(*[img.size for img in images])

    if not variable_height and not _all_equal(heights):
        raise ValueError('heights must be the same')

    out_w = sum(widths)
    out_h = max(heights)
    out = Image.new(images[0].mode, (out_w, out_h))
    cum_w = 0
    for w, img in zip(widths, images):
        out.paste(img, (cum_w, 0))
        cum_w += w
    return out


def dstack_rgb(images):
    """ stack PIL images in depth, as RGB channels.
    """
    # TODO auto fill-in None
    if not len(images) == 3:
        raise ValueError('need 3 images')
    out = Image.merge('RGB', images)
    return out


def square_montage(images, resize_mode='center', bg=None, border_color=None):
    """ create a square (as possible) montage. squareness is determined
    in terms of (rows, cols), not final montage size.

    :parameters:
        - images: list of PIL.Image
            input
        - resize_mode: string
            how to resize images. options: center, none
            if none, all images should be same size.

    TODO: adjustable borders

    >>> imgs = [Image.new('L', (128, 64)),
    ...         Image.new('L', (128, 64)),
    ...         Image.new('L', (128, 64))]
    >>> m = square_montage(imgs)
    >>> m.size
    (256, 128)
    >>> imgs = [Image.new('L', (128, 64)),
    ...         Image.new('L', (128, 64)),
    ...         Image.new('L', (128, 64)),
    ...         Image.new('L', (128, 64)),
    ...         Image.new('L', (128, 64))]
    >>> m = square_montage(imgs)
    >>> m.size
    (256, 192)

    """

    # TODO resize modes

    images = list(images)
    if bg is None:
        bg = _default_color(images[0].mode, 0)
    if border_color is None:
        border_color = _default_color(images[0].mode, 20, transparent=False)
    num_images = len(images)
    num_cols = int(round(np.sqrt(num_images)))
    num_rows = int(np.ceil(float(num_images)/num_cols))
    widths, heights = zip(*[img.size for img in images])
    w, h = max(widths), max(heights)
    montage = Image.new(images[0].mode, (num_cols*w, num_rows*h), bg)
    if resize_mode=='center':
        resized_images = [letterbox_resize(img, (w, h), bg) for img in images]
    elif resize_mode=='none':
        resized_images = images[:]
    else:
        raise ValueError('unknown resize_mode')
    for i, img in enumerate(resized_images):
        img = ImageOps.expand(img, 1, border_color)
        r, c = i/num_cols, i%num_cols
        x, y = c*w, r*h
        montage.paste(img, (x, y))
    return montage


def montage(images,
            nrows, ncols,
            margins_ltrb=(0, 0, 0, 0)):
    """
    :parameters:
        - images: sequence
            sequence of pil images
        - nrows: int
        - ncols: int
        - img_height_width: tuple(int, int)
            img dims
        - margins: tuple(int, int, int, int)
            margins for montage; left, top, right, bottom
        - padding: int
            padding between images
    """
    imgh, imgw = img_height_width
    (marl, mart, marr, marb) = margins_ltrb

    # calculate the size of the output image, based on the
    # photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (ncols*photow+marw+padw,nrows*photoh+marh+padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    inew = Image.new('RGB',isize,white)

    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            try:
                img = imgs.pop(0)
            except:
                break
            inew.paste(img,bbox)
    return inew


if __name__ == '__main__':
    import doctest
    flags = doctest.REPORT_NDIFF
    fail, total = doctest.testmod(optionflags=flags)
    print("{} failures out of {} tests".format(fail, total))

