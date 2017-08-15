import math


class ImgDims(object):
    """
    manage image dimensions.
    TODO: look at vigra python binding tag system.
    """

    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height


    @staticmethod
    def from_shape(shape):
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
