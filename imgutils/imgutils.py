import math

import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


def aspect_preserving_resize(img, w, h, bg=None):
    """
    Use PIL thumbnail to resize. May letterbox output.

    :parameters:
        - bg: tuple(int, int, int)
            color for background as rgb int tuple
    """
    img.thumbnail((w, h), Image.ANTIALIAS)
    if bg is None:
        bg=(255, 255, 255)
    newimg = Image.new(img.mode, (w, h), bg)
    left = int(math.floor((newimg.size[0]-img.size[0])*.5))
    top = int(math.floor((newimg.size[1]-img.size[1])*.5))
    newimg.paste(img, (left, top))
    return newimg


def smart_resize(img, w, h, interp=Image.CUBIC):
    """
    adjusts either w or h depending on which is None

    :parameters:
        - interp: int
            interpolation code from PIL.Image
    """
    old_w, old_h = img.size
    ratio = float(old_w)/old_h
    if h is None:
        h = int(w/ratio)
    elif w is None:
        w = int(h*ratio)
    img = img.resize((w, h), interp)
    return img


def center_paste_resize(img, w, h, bg=None):
    """
    resizes by pasting image in center.
    may do letterboxing.

    :parameters:
        - bg: tuple(int, int, int)
            color for background as rgb int tuple
    """
    if bg is None:
        bg=(255, 255, 255)
    if img.size[0] >= w or img.size[1] >= h:
        newimg = img.copy()
        newimg.thumbnail((w, h), Image.ANTIALIAS)
        return newimg
    newimg = Image.new(img.mode, (w, h), bg)
    left = int(math.floor((newimg.size[0]-img.size[0])*.5))
    top = int(math.floor((newimg.size[1]-img.size[1])*.5))
    #print w, h, img.size, left, top
    newimg.paste(img, (left, top))
    return newimg.copy()


def trim_percentage(img, percentage):
    """
    trim percentage off images

    :parameters:
        - percentage: int
            percentage of dimension to trim off.
            both sides are trimmed, half each side.
    """
    px_w = img.size[0]*(percentage/100.)
    px_h = img.size[1]*(percentage/100.)
    box = map(int, (px_w/2, px_h/2, img.size[0]-px_w/2, img.size[1]-px_h/2))
    img = img.crop(box)
    return img


def crop_center(img, width, height):
    """
    crop box of width x height from center of image.
    assumes box is smaller than image.
    """
    # box is left, upper, right, lower pixel
    # img.size is width, height
    # TODO what if crop box is bigger than img
    size = (width, height)
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


def draw_bbox(img, bb, color=(255, 0, 0)):
    draw = ImageDraw.ImageDraw(img)
    draw.rectangle(bb, fill=None, outline=color)
    return img


def add_border(img, px, color):
    return ImageOps.expand(img, px, color)


def hstack(images):
    """ stack PIL images downwards.
    """
    widths, heights = zip(*[img.size for img in images])

    out_w = max(widths)
    out_h = sum(heights)
    out = Image.new(images[0].mode, (out_w, out_h))
    cum_h = 0
    for h, img in zip(heights, images):
        out.paste(img, (0, cum_h))
        cum_h += h
    return out


def vstack(images):
    """ stack PIL images sideways.
    """
    widths, heights = zip(*[img.size for img in images])
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
    # TODO aut fill-in None
    if not len(images) == 3:
        raise ValueError('need 3 images')
    out = Image.merge('RGB', images)
    return out


def square_montage(images, resize_mode='max', bg=None, border_color=None):
    """ create a square (as possible) montage

    :parameters:
        - images: list of PIL.Image
            input
        - resize_mode: string
            how to resize images. options: max, center, none
            if none, all images should be same size.
    """
    # TODO resize modes
    if bg is None:
        bg = (0,0,0)
    if border_color is None:
        border_color = (20,20,20)
    num_images = len(images)
    num_cols = int(np.sqrt(num_images))
    num_rows = int(np.ceil(float(num_images)/num_cols))
    widths, heights = zip(*[img.size for img in images])
    w, h = max(widths), max(heights)
    montage = Image.new('RGB', (num_cols*w, num_rows*h), bg)
    if resize_mode=='max':
        resized_images = [aspect_preserving_resize(img, w, h, bg) for img in images]
    elif resize_mode=='center':
        resized_images = [center_paste_resize(img, w, h, bg) for img in images]
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


def montage(images, montage_rows_cols, img_height_width,
            margins_ltrb, padding):
    """
    adapted from activestate recipe

    :parameters:
        - images: list
            list of pil images
        - montage_rows_cols: tuple(int, int)
            out rows and cols
        - img_height_width: tuple(int, int)
            img dims
        - margins: tuple(int,int,int,int)
            margins for montage
        - padding: int
            padding between images
    """
    nrows, ncols = montage_rows_cols
    photoh, photow = img_height_width
    (marl,mart,marr,marb) = margins_ltrb

    # Calculate the size of the output image, based on the
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
