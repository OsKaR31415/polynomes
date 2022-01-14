
class SpecialZero:
    """Zero, but meant to be in a ZeroForever generator."""
    def __int__(self):
        return 0
    def __add__(self, other):
        return 0 + other
    def __radd__(self, other):
        return other + 0
    def __sub__(self, other):
        return 0 - other
    def __rsub__(self, other):
        return other - 0
    def __mul__(self, other):
        return 0 * other
    def __rmul__(self, other):
        return other * 0
    def __div__(self, other):
        return 0 / other
    def __rdiv__(self, other):
        raise other / 0
    def __str__(self):
        return "Ø"
    def __repr__(self):
        return "SpecialZero()"

class ZeroForever:
    """Class to represent an infinity of SpecialZero."""
    def __next__(self):
        return SpecialZero()
    def __str__(self):
        return "(Ø...)"
    def __repr__(self):
        return "ZeroForever()"
    def __iter__(self):
        return self
