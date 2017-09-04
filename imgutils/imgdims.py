
__all__ = ['ImgDims']


import math


class ImgDims(object):
    """
    manage image dimensions.

    >>> d = ImgDims(320, 240)
    >>> d.width
    320
    >>> d.height
    240
    >>> d = ImgDims.from_shape([240, 320])
    >>> d
    ImgDims(width=320, height=240)
    >>> d2 = ImgDims(10, 20)
    >>> d + d2
    ImgDims(width=330, height=260)
    >>> d*2
    ImgDims(width=640, height=480)
    >>> 2*d
    ImgDims(width=640, height=480)
    >>> d*2 == ImgDims(640, 480)
    True
    >>> d == ImgDims(640, 480)
    False
    >>> d.rows
    240
    >>> d.cols
    320
    >>> d/2
    ImgDims(width=160, height=120)
    >>> df = ImgDims(width=320.3, height=239.8)
    >>> df.round()
    ImgDims(width=320, height=240)
    >>> df.floor()
    ImgDims(width=320, height=239)
    >>> d.tolist()
    [320, 240]
    >>> d.toshape()
    (240, 320)
    """

    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height

    @staticmethod
    def from_shape(shape):
        """ from numpy ndarry shape """
        return ImgDims(width=shape[1], height=shape[0])

    def __repr__(self):
        return 'ImgDims(width={}, height={})'.format(self.width, self.height)

    def __add__(self, other):
        if isinstance(other, ImgDims):
            return ImgDims(self.width + other.width,
                           self.height + other.height)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return ImgDims(self.width + other[0],
                           self.height + other[1])

    __radd__ = __add__

    def __iadd__(self, other):
        self.width += other.width
        self.height += other.height

    def __sub__(self, other):
        if isinstance(other, ImgDims):
            return ImgDims(self.width - other.width,
                           self.height - other.height)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return ImgDims(self.width - other[0],
                           self.height - other[1])

    def __rsub__(self, other):
        if isinstance(other, ImgDims):
            return ImgDims(other.width - self.width,
                           other.height - self.height)
        else:
            assert hasattr(other, '__len__') and len(other) == 2
            return ImgDims(other[0] - self.width,
                           other[1] - self.height)

    def __mul__(self, other):
        return ImgDims(self.width * other,
                       self.height * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        self.width *= other
        self.height *= other
        return self

    def __div__(self, other):
        return ImgDims(self.width / other,
                       self.height / other)

    __rdiv__ = __div__

    def __idiv__(self, other):
        self.width /= other
        self.height /= other
        return self

    def __eq__(self, other):
        return other.width == self.width and other.height == self.height

    def __iter__(self):
        yield self.width
        yield self.height

    @property
    def rows(self):
        return self.height

    @property
    def cols(self):
        return self.width

    def round(self):
        return ImgDims(int(round(self.width)),
                       int(round(self.height)))

    def floor(self):
        return ImgDims(int(math.floor(self.width)),
                       int(math.floor(self.height)))

    def ceil(self):
        return ImgDims(int(math.floor(self.width)),
                       int(math.floor(self.height)))

    def tolist(self):
        return [self.width, self.height]

    def toshape(self):
        """ to numpy ndarray shape. """
        return (self.height, self.width)

if __name__ == '__main__':
    import doctest
    flags = doctest.REPORT_NDIFF
    fail, total = doctest.testmod(optionflags=flags)
    print("{} failures out of {} tests".format(fail, total))

