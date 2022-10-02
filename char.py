class RangeError (ValueError): pass
class LengthError (ValueError): pass

class Char (int):
    '''
    An ASCII character (integer of maximum 1 byte length and range 0..127)

    Behaves like a normal integer in operations and comparisons.

    Can be created in following ways:
        Char()      # NULL character
        Char(0)     # NULL character
        Char(None)  # NULL character
        Char('a')   # 'a'  character
        Char(97)    # 'a'  character
        Char(97.3)  # 'a'  character
        Char(14)    # non-pritable but valid ASCII character
        Char(127)   # non-pritable but valid ASCII character
        Char(158)   # invalid character (raises RangeError)
        Char(-97)   # invalid character (raises RangeError)

    Range can be changed to -128..255 by providing strict=False
        Char(-129, strict=False)  # raises RangeError
        Char(-128, strict=False)  # does NOT raise RangeError
        Char(-10,  strict=False)  # does NOT raise RangeError
        Char(228,  strict=False)  # does NOT raise RangeError
        Char(255,  strict=False)  # does NOT raise RangeError
        Char(256,  strict=False)  # raises RangeError

    Non-strict Chars can be transformed into signed and unsigned form (keeping the underlying bits same).
        Char(130,  strict=False).signed   # Char(-126)
        Char(130,  strict=False).usigned  # Char(130)
        Char(-110, strict=False).signed   # Char(-110)
        Char(-110, strict=False).usigned  # Char(146)
    Normal Chars are not affected by this.
        Char(65)            # Char('A')
        Char(65).signed     # Char('A')
        Char(65).unsigned   # Char('A')

    Helper function `join(iterable)` can join multiple Chars into a string.
    For example, following code
        my_string = join([Char('a'), Char('b'), Char('c')])
        prin(my_string)
    Prints
        abc
    '''

    def __new__ (klass, value=None, *, strict=True):
        if value is None:
            return int.__new__(klass, 0)
        elif isinstance (value, str):
            if len(value) == 1:
                if len(value.encode()) == 1:
                    return int.__new__(klass, ord(value))
                else:
                    raise ValueError ('Only ASCII characters allowed')
            else:
                raise LengthError ('Provided str argument must be of length 1')
        else:
            result = int.__new__(klass, value)

            minimum = 0
            maximum = 127
            if not strict:
                minimum = -128
                maximum =  256

            if minimum <= result <= maximum:
                return result
            else:
                raise RangeError (f'Value must be in range({minimum}, {maximum})')

    def __str__ (self, /):
        return chr(self.unsigned)

    def __repr__ (self, /):
        if self < 0 or self.__str__().__repr__().startswith('\'\\x'):
            return self.__class__.__name__ + '(' + repr(int(self)) + ')'
        return self.__class__.__name__ + '(' + chr(self).__repr__() + ')'

    @property
    def signed (self):
        if self > 127:
            return self.__class__(self - 256)
        return self

    @property
    def unsigned (self):
        if self < 0:
            return self.__class__(self + 256)
        return self


def join (iterable, /):
    '''Join Chars in an interable into a string'''
    result = ''
    for index, item in enumerate(iterable):
        if isinstance(item, Char):
            result += str(item)
        else:
            raise TypeError (f"Cannot join object of type '{type(item)}' at index {index} of provided iterable. Only objects of type 'Char' can be joined.")

    return result
